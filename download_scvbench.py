import yt_dlp
import os
import json

def download_video(number, video_id, url, path):
    # 确保保存路径存在
    os.makedirs(path, exist_ok=True)

    ydl_opts = {
        'outtmpl': f'{path}/{video_id}.mp4',
        'format': 'best',
        'retries': 3,
    }

    try:
        filename = f"{video_id}.mp4"
        if filename in os.listdir(path):
            print(f"{number} 视频已存在: {filename}")
            return

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print(f"{number} 视频下载成功: {video_id}")

    except Exception as e:
        print(f"{number} 下载失败 ({video_id}): {e}")
        with open(r'your path to fail.txt', 'a', encoding='utf-8') as log:  # todo
            log.write(f'{number} 下载失败: {url}\n')


# JSONL 文件路径
jsonl_path = r'your path to data.jsonl'  # todo
save_path = r'your path to video'  # todo

# 逐行读取 JSONL
with open(jsonl_path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        line = line.strip()
        if not line:
            continue  # 跳过空行

        try:
            sample = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"第 {i+1} 行 JSON 解析失败: {e}")
            continue

        video_id = sample.get('video_id')
        if not video_id:
            print(f"第 {i+1} 行缺少 video_id，跳过")
            continue

        # 尝试获取 video_url，如果没有，则构造 YouTube 链接
        video_url = sample.get('video_url')
        if not video_url:
            video_url = f"https://www.youtube.com/watch?v={video_id}"

        download_video(i + 1, video_id, video_url, save_path)