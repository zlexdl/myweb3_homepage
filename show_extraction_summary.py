#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
显示PPT提取结果的统计信息
"""

import os
from pathlib import Path


def count_files_in_dir(dir_path):
    """统计目录中的文件数量"""
    if not os.path.exists(dir_path):
        return 0
    files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    return len(files)


def get_statistics(base_dir, lang_name):
    """获取提取结果的统计信息"""
    print(f"\n{lang_name}PPT ({base_dir})")
    print("=" * 60)
    
    base_path = Path(base_dir)
    if not base_path.exists():
        print(f"错误: 目录 {base_dir} 不存在")
        return
    
    # 统计所有slide文件夹
    slide_dirs = sorted([d for d in base_path.iterdir() if d.is_dir() and d.name.startswith('slide_')])
    
    total_slides = len(slide_dirs)
    slides_with_images = 0
    slides_without_images = 0
    total_images = 0
    total_texts = 0
    
    for slide_dir in slide_dirs:
        images_dir = slide_dir / "images"
        texts_dir = slide_dir / "texts"
        
        image_count = count_files_in_dir(images_dir)
        text_count = count_files_in_dir(texts_dir)
        
        if image_count > 0:
            slides_with_images += 1
            total_images += image_count
        else:
            slides_without_images += 1
        
        if text_count > 0:
            total_texts += text_count
    
    print(f"总页数: {total_slides}")
    print(f"包含图片的页面: {slides_with_images}")
    print(f"没有图片的页面: {slides_without_images}")
    print(f"总图片数: {total_images}")
    print(f"总文本文件数: {total_texts}")
    
    # 找出图片最多的页面
    max_images = 0
    max_images_slide = None
    for slide_dir in slide_dirs:
        images_dir = slide_dir / "images"
        image_count = count_files_in_dir(images_dir)
        if image_count > max_images:
            max_images = image_count
            max_images_slide = slide_dir.name
    
    if max_images > 0:
        print(f"图片最多的页面: {max_images_slide} ({max_images}张图片)")


def main():
    print("=" * 60)
    print("PPT内容提取统计")
    print("=" * 60)
    
    get_statistics("extracted_en", "英文")
    get_statistics("extracted_cn", "中文")
    
    print("\n" + "=" * 60)
    print("统计完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

