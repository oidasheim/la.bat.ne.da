"""
Hardware Optimizer Module
Detects and optimizes for available hardware

Features:
- Hardware detection (CPU, GPU, RAM)
- Automatic optimization for weak/strong hardware
- GPU support (CUDA, OpenCL, Metal)
- Memory-efficient processing
"""

import platform
from typing import Dict, Optional

class HardwareDetector:
    """Detects system hardware capabilities"""
    
    @staticmethod
    def detect_system() -> Dict:
        """Detect available hardware"""
        hardware = {
            "os": platform.system(),
            "cpu": HardwareDetector._detect_cpu(),
            "gpu": HardwareDetector._detect_gpu(),
            "ram": HardwareDetector._detect_ram(),
            "storage": HardwareDetector._detect_storage()
        }
        return hardware
    
    @staticmethod
    def _detect_cpu() -> Dict:
        """Detect CPU information"""
        cpu_info = {
            "cores": 0,
            "threads": 0,
            "brand": None
        }
        
        try:
            import psutil
            cpu_info["cores"] = psutil.cpu_count(logical=False)
            cpu_info["threads"] = psutil.cpu_count(logical=True)
        except ImportError:
            pass
        
        try:
            import platform
            cpu_info["brand"] = platform.processor()
        except:
            pass
        
        return cpu_info
    
    @staticmethod
    def _detect_gpu() -> Dict:
        """Detect GPU capabilities"""
        gpu_info = {
            "available": False,
            "type": None,
            "memory_mb": 0
        }
        
        # Check for CUDA
        try:
            import torch
            if torch.cuda.is_available():
                gpu_info["available"] = True
                gpu_info["type"] = "CUDA"
                gpu_info["memory_mb"] = torch.cuda.get_device_properties(0).total_memory / (1024**2)
        except ImportError:
            pass
        
        # Check for Metal (Apple Silicon)
        if platform.system() == "Darwin":
            try:
                import torch
                if torch.backends.mps.is_available():
                    gpu_info["available"] = True
                    gpu_info["type"] = "Metal"
            except:
                pass
        
        return gpu_info
    
    @staticmethod
    def _detect_ram() -> Dict:
        """Detect available RAM"""
        ram_info = {
            "total_mb": 0,
            "available_mb": 0
        }
        
        try:
            import psutil
            ram = psutil.virtual_memory()
            ram_info["total_mb"] = ram.total / (1024**2)
            ram_info["available_mb"] = ram.available / (1024**2)
        except ImportError:
            pass
        
        return ram_info
    
    @staticmethod
    def _detect_storage() -> Dict:
        """Detect storage information"""
        storage_info = {
            "total_mb": 0,
            "free_mb": 0
        }
        
        try:
            import shutil
            stat = shutil.disk_usage("/")
            storage_info["total_mb"] = stat.total / (1024**2)
            storage_info["free_mb"] = stat.free / (1024**2)
        except:
            pass
        
        return storage_info

class HardwareOptimizer:
    """Optimizes processing based on available hardware"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.hardware = HardwareDetector.detect_system()
    
    def get_optimization_profile(self) -> Dict:
        """Determine optimal settings based on hardware"""
        profile = {
            "processing_mode": self._determine_processing_mode(),
            "chunk_size": self._determine_chunk_size(),
            "batch_size": self._determine_batch_size(),
            "max_threads": self._determine_max_threads(),
            "use_gpu": self.hardware["gpu"]["available"],
            "memory_limit_mb": self._determine_memory_limit()
        }
        
        if self.verbose:
            print(f"\n🖥️ Hardware Optimization Profile:")
            print(f"  Processing Mode: {profile['processing_mode']}")
            print(f"  Chunk Size: {profile['chunk_size']}")
            print(f"  Batch Size: {profile['batch_size']}")
            print(f"  Max Threads: {profile['max_threads']}")
            print(f"  GPU Available: {profile['use_gpu']}")
            print(f"  Memory Limit: {profile['memory_limit_mb']} MB")
        
        return profile
    
    def _determine_processing_mode(self) -> str:
        """Determine if should use GPU, CPU, or hybrid"""
        if self.hardware["gpu"]["available"]:
            return "gpu_accelerated"
        
        cpu_cores = self.hardware["cpu"]["cores"]
        if cpu_cores >= 8:
            return "multi_threaded"
        else:
            return "single_threaded"
    
    def _determine_chunk_size(self) -> int:
        """Determine optimal chunk size for processing"""
        ram_mb = self.hardware["ram"]["available_mb"]
        
        if ram_mb > 16000:
            return 1024  # 1GB chunks
        elif ram_mb > 8000:
            return 512   # 512MB chunks
        else:
            return 256   # 256MB chunks
    
    def _determine_batch_size(self) -> int:
        """Determine optimal batch size"""
        if self.hardware["gpu"]["available"]:
            gpu_mem = self.hardware["gpu"]["memory_mb"]
            return max(1, int(gpu_mem / 512))  # Assume 512MB per batch
        else:
            cpu_threads = self.hardware["cpu"]["threads"]
            return max(1, cpu_threads // 2)
    
    def _determine_max_threads(self) -> int:
        """Determine maximum threads to use"""
        cpu_threads = self.hardware["cpu"]["threads"]
        
        # Leave some threads for system
        return max(1, cpu_threads - 2)
    
    def _determine_memory_limit(self) -> int:
        """Determine safe memory limit"""
        available_mb = self.hardware["ram"]["available_mb"]
        
        # Use 70% of available memory
        return int(available_mb * 0.7)

def optimize_for_hardware(verbose=False) -> Dict:
    """Main function to optimize for current hardware"""
    optimizer = HardwareOptimizer(verbose=verbose)
    return optimizer.get_optimization_profile()
