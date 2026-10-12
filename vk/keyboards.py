# from vkbottle import Keyboard, KeyboardButtonColor, Callback

# ITEMS_PER_PAGE = 6

# def group_selection_kb(groups: list[str], page: int = 0) -> Keyboard:
#     kb = Keyboard(inline=True)
#     start_idx = page * ITEMS_PER_PAGE
#     end_idx = start_idx + ITEMS_PER_PAGE
#     cur_names = groups[start_idx:end_idx]

#     for i, name in enumerate(cur_names):
#         kb.add(Callback(name, payload={"act": "select_group", "name": name}), color=KeyboardButtonColor.PRIMARY)
#         if (i + 1) % 2 == 0 and (i + 1) != len(cur_names):
#             kb.row()

#     kb.row()
#     total_pages = (len(groups) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
#     if page > 0:
#         kb.add(Callback("<- Назад", payload={"act": "nav_groups", "page": page - 1}), color=KeyboardButtonColor.SECONDARY)
#     if (page + 1) < total_pages:
#         kb.add(Callback("Вперёд ->", payload={"act": "nav_groups", "page": page + 1}), color=KeyboardButtonColor.SECONDARY)
    
#     kb.row()
#     kb.add(Callback("Закрыть", payload={"act": "close"}), color=KeyboardButtonColor.NEGATIVE)
#     return kb

# def close_kb() -> Keyboard:
#     kb = Keyboard(inline=True)
#     kb.add(Callback("Закрыть", payload={"act": "close"}), color=KeyboardButtonColor.NEGATIVE)
#     return kb

#imports
import re

from vkbottle import Keyboard, KeyboardButtonColor, Callback
from services.database import async_session, Database


#CONSTANTS
ITEMS_PER_PAGE = 6

#inits
db = Database(async_session)

#------------------- KEYBOARDS -------------------''

# keyboard for group selection with pagination
def join_kb(page: int = 0) -> Keyboard:
    kb = Keyboard(inline = True)

    groups = db.groups.get_all_by()
    codes = [re.sub(r"\D", "", g.code) for g in groups]

    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE

    for i, code in enumerate(codes):
        kb.add(Callback(code, payload={"act": "select_group", "name": code}), color=KeyboardButtonColor.PRIMARY)
        if (i + 1) % 2 == 0 and (i + 1) != len(codes):
            kb.row()
    
    kb.row()
    total_pages = (len(codes) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    if page > 0:
        kb.add(Callback("<= Назад", payload={"act": "nav_groups", "page": page - 1}), color=KeyboardButtonColor.SECONDARY)
    if (page + 1) < total_pages:
        kb.add(Callback("Вперёд =>", payload={"act": "nav_groups", "page": page + 1}), color=KeyboardButtonColor.SECONDARY)
    
    kb.row()
    kb.add(Callback("Закрыть", payload={"act": "close"}), color=KeyboardButtonColor.NEGATIVE)
    return kb

# keyboard for closing nav bars or messages
def close_kb() -> Keyboard:
    kb = Keyboard(inline=True)
    kb.add(
        Callback("Закрыть",payload={"act":"close"}),
        color=KeyboardButtonColor.NEGATIVE
    )
    return kb

# keyboard undo
def back_kb(prev_act: str | None = None) -> Keyboard:
    kb = Keyboard(inline=True)
    kb.add(
        Callback("<= Назад", payload={"act":"back", "prev_act":prev_act}),
        color=KeyboardButtonColor.NEGATIVE
    )
    return kb

# keyboard for review
def review_kb(object: str | None = None) -> Keyboard:
    kb = Keyboard(inline = True)
    kb.add(
        Callback("Да", payload = {"act":"confirm", "object": object}),
        color = KeyboardButtonColor.POSITIVE
    )

    kb.add(
        Callback("Нет", payload = {"act":"deny", "object": object}),
        color = KeyboardButtonColor.NEGATIVE
    )
    return kb


