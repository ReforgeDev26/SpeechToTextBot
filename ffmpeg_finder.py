"""
Модуль для поиска FFmpeg в системе.
Поддерживает Windows, macOS и Linux.
"""

import os
import sys
import logging
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Tuple, Dict

# Настройка логирования
logger = logging.getLogger(__name__)


class FFmpegFinder:
    """
    Класс для поиска и проверки FFmpeg в системе.
    """
    
    def __init__(self):
        self.is_windows = sys.platform.startswith('win')
        self.is_mac = sys.platform.startswith('darwin')
        self.is_linux = sys.platform.startswith('linux')
        self.ffmpeg_exe = 'ffmpeg.exe' if self.is_windows else 'ffmpeg'
        
    def find(self) -> Optional[str]:
        """
        Основной метод поиска FFmpeg.
        
        Returns:
            Путь к FFmpeg или None, если не найден
        """
        logger.info("🔍 Поиск FFmpeg в системе...")
        
        # Пробуем разные методы поиска по порядку
        finders = [
            self._find_in_path,
            self._find_in_common_locations,
            self._find_in_current_dir,
            self._find_via_shell_command
        ]
        
        for finder in finders:
            path = finder()
            if path:
                logger.info(f"✅ FFmpeg найден: {path}")
                return path
        
        logger.error("❌ FFmpeg не найден в системе")
        return None
    
    def _find_in_path(self) -> Optional[str]:
        """Поиск в переменной PATH"""
        path = shutil.which('ffmpeg')
        if path:
            logger.debug(f"Найден в PATH: {path}")
        return path
    
    def _find_in_common_locations(self) -> Optional[str]:
        """Поиск в стандартных местах установки"""
        locations = self._get_common_locations()
        
        for location in locations:
            path = Path(location)
            if path.exists():
                logger.debug(f"Найден в стандартном месте: {location}")
                return str(path)
        
        # Дополнительно проверяем пути из PATH для Windows
        if self.is_windows:
            return self._check_windows_path_dirs()
        
        return None
    
    def _get_common_locations(self) -> list:
        """Возвращает список стандартных мест установки для текущей ОС"""
        home = str(Path.home())
        
        if self.is_windows:
            return [
                r'C:\ffmpeg\bin\ffmpeg.exe',
                r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
                r'C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe',
                rf'{home}\ffmpeg\bin\ffmpeg.exe',
                rf'{home}\scoop\apps\ffmpeg\current\bin\ffmpeg.exe',
                rf'{home}\AppData\Local\Microsoft\WinGet\packages\ffmpeg.exe',
            ]
        
        if self.is_mac:
            return [
                '/usr/local/bin/ffmpeg',
                '/opt/homebrew/bin/ffmpeg',
                '/usr/bin/ffmpeg',
                f'{home}/bin/ffmpeg',
                '/opt/local/bin/ffmpeg',  # MacPorts
            ]
        
        if self.is_linux:
            return [
                '/usr/bin/ffmpeg',
                '/usr/local/bin/ffmpeg',
                '/opt/ffmpeg/bin/ffmpeg',
                f'{home}/bin/ffmpeg',
                '/snap/bin/ffmpeg',
                '/app/bin/ffmpeg',
            ]
        
        return []
    
    def _check_windows_path_dirs(self) -> Optional[str]:
        """Проверяет директории из PATH на наличие ffmpeg.exe"""
        path_env = os.environ.get('PATH', '')
        
        for dir_path in path_env.split(';'):
            if not dir_path.strip():
                continue
                
            potential_path = Path(dir_path) / 'ffmpeg.exe'
            if potential_path.exists():
                logger.debug(f"Найден в директории из PATH: {potential_path}")
                return str(potential_path)
        
        return None
    
    def _find_in_current_dir(self) -> Optional[str]:
        """Поиск в текущей директории и поддиректориях"""
        current_dir = Path.cwd()
        
        # Проверяем в текущей директории
        local_path = current_dir / self.ffmpeg_exe
        if local_path.exists():
            logger.debug(f"Найден в текущей директории: {local_path}")
            return str(local_path)
        
        # Проверяем в ./ffmpeg/bin
        local_bin_path = current_dir / 'ffmpeg' / 'bin' / self.ffmpeg_exe
        if local_bin_path.exists():
            logger.debug(f"Найден в ./ffmpeg/bin: {local_bin_path}")
            return str(local_bin_path)
        
        return None
    
    def _find_via_shell_command(self) -> Optional[str]:
        """Поиск через системные команды which/where"""
        try:
            if self.is_windows:
                result = subprocess.run(
                    ['where', 'ffmpeg'], 
                    capture_output=True, 
                    text=True, 
                    shell=True
                )
            else:
                result = subprocess.run(
                    ['which', 'ffmpeg'], 
                    capture_output=True, 
                    text=True
                )
            
            if result.returncode == 0 and result.stdout.strip():
                path = result.stdout.strip().split('\n')[0]
                logger.debug(f"Найден через which/where: {path}")
                return path
                
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        return None


# Создаем экземпляр для удобного импорта
_finder = FFmpegFinder()

# Функции для использования
def find_ffmpeg() -> Optional[str]:
    """Найти FFmpeg в системе"""
    return _finder.find()
