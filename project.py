import os
import re
import edge_tts
import speech_recognition as sr
from pydub import AudioSegment
import asyncio

# 配置
INPUT_TEXT_FILE = "你的文本.txt"  # 请替换为你的文本文件路径
OUTPUT_DIR = "output_audios"
TTS_VOICE = "en-US-AriaNeural"  # 英文语音

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_sentences(text_file):
    """从文本中提取需要转换的句子"""
    with open(text_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sentences = []
    
    # 按行处理
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        
        # 跳过空行
        if not line:
            continue
            
        # 跳过标题行（包含emoji、括号等）
        if any(char in line for char in ['🏞', '(', ')', 'Set ']):
            continue
            
        # 匹配以数字加点开头的句子（如 "1.Welcome to..."）
        match = re.match(r'^(\d+)\.\s*(.+)$', line)
        if match:
            sentence = match.group(2).strip()
            if sentence:  # 确保句子不为空
                sentences.append(sentence)
    
    return sentences

async def text_to_speech(text, voice=TTS_VOICE):
    """将单句文本转换为音频文件"""
    # 使用句子内容创建安全文件名
    safe_name = re.sub(r'[^\w\s-]', '', text)[:100].strip().replace(' ', '_')
    output_path = os.path.join(OUTPUT_DIR, f"{safe_name}.mp3")
    
    # 如果文件已存在，添加序号避免覆盖
    counter = 1
    original_path = output_path
    while os.path.exists(output_path):
        name, ext = os.path.splitext(original_path)
        output_path = f"{name}_{counter}{ext}"
        counter += 1
    
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    print(f"已生成: {os.path.basename(output_path)}")
    return output_path

async def main():
    # 提取需要转换的句子
    sentences = extract_sentences(INPUT_TEXT_FILE)
    print(f"共提取出 {len(sentences)} 个句子需要转换。")
    
    if not sentences:
        print("未找到需要转换的句子，请检查文本格式。")
        return
    
    # 显示提取的句子
    print("提取的句子列表：")
    for i, sentence in enumerate(sentences, 1):
        print(f"{i}. {sentence}")
    
    # 批量转换TTS
    print("\n开始生成音频文件...")
    tasks = []
    for sentence in sentences:
        tasks.append(text_to_speech(sentence))
    
    await asyncio.gather(*tasks)
    print(f"\n所有音频文件已生成到 '{OUTPUT_DIR}' 目录。")

if __name__ == "__main__":
    asyncio.run(main())