from aiogram.utils.callback_data import CallbackData

choose_formation_cd = CallbackData('formation', 'formation')
choose_song_cd = CallbackData('song', 'song_id')
delete_song_cd = CallbackData('delete', 'song_id')
view_chords_cd = CallbackData('view_chords', 'song_id')
new_cover_cd = CallbackData('new_cover', 'song_id')
send_song_cd = CallbackData('send_song', 'song_id')
get_covers_cd = CallbackData('get_covers', 'song_id')
choose_cover_cd = CallbackData('choose_cover', 'cover_id')
send_cover_cd = CallbackData('send_cover', 'cover_id')
delete_cover_cd = CallbackData('delete_cover', 'cover_id')
choose_friend_cd = CallbackData('choose_friend', 'friend_id')
get_friend_songs_cd = CallbackData('get_friend_songs', 'friend_id')
