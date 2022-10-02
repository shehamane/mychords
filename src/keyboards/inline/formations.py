from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.guitar_config import formations
from utils.callback_datas import choose_formation_cd

formations_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=formation, callback_data=choose_formation_cd.new(formation=formation))]
        for formation in formations
    ]
)
