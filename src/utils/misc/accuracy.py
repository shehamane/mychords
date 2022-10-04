import autochord
from utils.db_api.api import db_api as db


async def calculate_accuracy(cover_path, song_id):
    cover_chords = autochord.recognize(cover_path)
    song_chords = await db.get_song_chords(song_id)

    cover_len = cover_chords[-1][1]
    truth_len = cover_len

    i = 0
    j = 0
    while i < len(cover_chords) - 1 and j < len(song_chords) - 1:
        curr_cover_chord = cover_chords[i][2]
        if curr_cover_chord == 'N':
            i += 1
            continue
        curr_song_chord = song_chords[j].name
        if curr_song_chord == 'N':
            j += 1
            continue

        if cover_chords[i + 1][0] < song_chords[j + 1].start:
            i += 1
        else:
            j += 1

        if curr_cover_chord != curr_song_chord:
            truth_len -= abs(cover_chords[i][0] - song_chords[j].start)

    return (truth_len / cover_len) * 100


# def calculate_accuracy(cover_path, song_path):
#     cover_chords = autochord.recognize(cover_path)
#     song_chords = autochord.recognize(song_path)
#
#     cover_len = cover_chords[-1][1]
#     truth_len = cover_len
#
#     i = 0
#     j = 0
#     while i < len(cover_chords) - 1 and j < len(song_chords) - 1:
#         curr_cover_chord = cover_chords[i][2]
#         if curr_cover_chord == 'N':
#             i += 1
#             continue
#         curr_song_chord = song_chords[j][2]
#         if curr_song_chord == 'N':
#             j += 1
#             continue
#
#         if cover_chords[i + 1][0] < song_chords[j + 1][0]:
#             i += 1
#         else:
#             j += 1
#
#         if curr_cover_chord != curr_song_chord:
#             truth_len -= abs(cover_chords[i][0] - song_chords[j][0])
#
#     return (truth_len / cover_len) * 100
