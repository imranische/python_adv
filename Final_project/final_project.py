from copy import deepcopy
import logging
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)
import os

# os.environ['TG_TOKEN'] = Here was my token, but it's private

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger('httpx').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# get token using BotFather
TOKEN = os.getenv('TG_TOKEN')

CONTINUE_GAME, FINISH_GAME = range(2)

FREE_SPACE = '.'
CROSS = 'X'
ZERO = 'O'


DEFAULT_STATE = [[FREE_SPACE for _ in range(3)] for _ in range(3)]


def get_default_state():
    """Helper function to get default state of the game"""
    return deepcopy(DEFAULT_STATE)


def generate_keyboard(state: list[list[str]]) -> list[list[InlineKeyboardButton]]:
    """Generate tic tac toe keyboard 3x3 (telegram buttons)"""
    return [
        [
            InlineKeyboardButton(state[r][c], callback_data=f'{r}{c}')
            for r in range(3)
        ]
        for c in range(3)
    ]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    context.user_data['keyboard_state'] = get_default_state()
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f'Ваш ход! Поставьте крестик в любой свободной кнопке', reply_markup=reply_markup)
    return CONTINUE_GAME


async def update_message(update: Update, context: ContextTypes.DEFAULT_TYPE, new_text: str) -> None:
    keyboard = generate_keyboard(context.user_data["keyboard_state"])
    await update.callback_query.edit_message_text(
        text=new_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Main processing of the game"""
    state = context.user_data["keyboard_state"]

    row, column = map(int, update.callback_query.data)
    if state[row][column] is not FREE_SPACE:
        return CONTINUE_GAME
    state[row][column] = CROSS
    if won(state):
        await update_message(
            update, context, "Поздравляем, вы победили! Нажмите /start для начала новой игры"
        )
        return FINISH_GAME

    zero_free_places = [
        (c, r) for r in range(3) for c in range(3) if state[c][r] is FREE_SPACE
    ]
    if not zero_free_places:
        await update_message(
            update, context, "Ничья! Нажмите /start для начала новой игры"
        )
        return FINISH_GAME

    row, column = random.choice(zero_free_places)
    state[row][column] = ZERO
    if won(state):
        await update_message(
            update, context, f"К сожалению, вы проиграли! Верим, что вам удастся победить в следующий раз."
            f"Нажмите /start для начала новой игры"
        )
        return FINISH_GAME

    await update_message(
        update, context, "Ваш ход! Поставьте крестик в любой свободной кнопке"
    )
    return CONTINUE_GAME


def won(fields: list[str]) -> bool:
    """Check if crosses or zeros have won the game"""
    win_positions = [
        # horizontals
        [[0, 0], [0, 1], [0, 2]],
        [[1, 0], [1, 1], [1, 2]],
        [[2, 0], [2, 1], [2, 2]],
        # verticals
        [[0, 0], [1, 0], [2, 0]],
        [[0, 1], [1, 1], [2, 1]],
        [[0, 2], [1, 2], [2, 2]],
        # diagonals
        [[0, 0], [1, 1], [2, 2]],
        [[2, 0], [1, 1], [0, 2]]
    ]

    # Field indices
    # 00 01 02
    # 10 11 12
    # 20 21 22

    for win in win_positions:
        if all((fields[win[0][0]][win[0][1]] == CROSS,
               fields[win[1][0]][win[1][1]] == CROSS,
               fields[win[2][0]][win[2][1]] == CROSS)):
            return True
        if all((fields[win[0][0]][win[0][1]] == ZERO,
               fields[win[1][0]][win[1][1]] == ZERO,
               fields[win[2][0]][win[2][1]] == ZERO)):
            return True

    return False


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    # reset state to default so you can play again with /start
    context.user_data['keyboard_state'] = get_default_state()
    return ConversationHandler.END


def main() -> None:
    """Run the bot"""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Setup conversation handler with the states CONTINUE_GAME and FINISH_GAME
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CONTINUE_GAME: [
                CallbackQueryHandler(game, pattern='^' + f'{r}{c}' + '$')
                for r in range(3)
                for c in range(3)
            ],
            FINISH_GAME: [
                CallbackQueryHandler(end, pattern='^' + f'{r}{c}' + '$')
                for r in range(3)
                for c in range(3)
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
