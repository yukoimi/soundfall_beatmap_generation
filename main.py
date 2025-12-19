import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
try:
    from mutagen import File
except ImportError:
    print("请先安装 mutagen 库: pip install mutagen")
    exit()

def generate_beat_labels():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="请选择音频文件",
        filetypes=[("Audio Files", "*.mp3 *.wav *.flac *.ogg *.m4a"), ("All Files", "*.*")]
    )

    if not file_path:
        print("未选择文件，程序退出。")
        return

    try:
        audio = File(file_path)
        if audio is None:
            messagebox.showerror("错误", "无法识别该音频格式！")
            return
        
        duration = audio.info.length
        filename_base = os.path.splitext(os.path.basename(file_path))[0]
        dir_path = os.path.dirname(file_path)

        bpm = simpledialog.askfloat("输入参数", f"检测到音频时长: {duration:.2f}秒\n\n请输入 BPM:", minvalue=1.0, maxvalue=999.0)
        if bpm is None: return

        offset = simpledialog.askfloat("输入参数", "请输入 Offset (起始偏移秒数):", minvalue=0.0, initialvalue=0.0)
        if offset is None: return
        
        beat_interval = 60.0 / bpm
        output_txt_path = os.path.join(dir_path, f"{filename_base}.txt")
        
        count = 0
        current_time = offset
        
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            while current_time <= duration:
                count += 1
                label_text = f"{count:02d}标签"
                line = f"{current_time:.6f}\t{current_time:.6f}\t{label_text}\n"
                f.write(line)
                
                current_time += beat_interval

        messagebox.showinfo("成功", f"处理完成！\n\n已生成: {count} 个标签\n文件保存为: {output_txt_path}")

    except Exception as e:
        messagebox.showerror("错误", f"发生意外错误:\n{str(e)}")

if __name__ == "__main__":
    generate_beat_labels()
