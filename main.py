import importlib.util
import sys
import subprocess

# Проверяем наличие библиотеки pytube
if importlib.util.find_spec("pytube") is None:
    print("Библиотека pytube не найдена. Устанавливаем...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pytube"])
else:
    print("Библиотека pytube уже установлена.")

from pytube import YouTube
import os

# Функция для скачивания видео
def download_video(video_url, output_path):
    try:
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=output_path)
        print("Видео успешно скачано.")
    except Exception as e:
        print(f"Ошибка при скачивании видео: {e}")

# Основной код программы
if __name__ == "__main__":
    # Запрос ссылки на видео
    video_url = input("Введите ссылку на видео: ")

    # Запрос пути для сохранения видео
    output_path = input("Введите путь для сохранения видео (Он запомнится, до перезапуска программы.): ")

    # Проверка существования пути
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Скачивание видео
    download_video(video_url, output_path)

    # Сохранение пути для следующего запуска
    with open('path.txt', 'w') as f:
        f.write(output_path)

    # Запрос новой ссылки на видео
    while True:
        video_url = input("Введите ссылку на видео для скачивания: ")
        if video_url.lower() == "exit":
            break
        download_video(video_url, output_path)
