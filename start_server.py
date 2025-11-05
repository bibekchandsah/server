#!/usr/bin/env python3
"""
Quick Start Script for Unified File Server
Automatically uses the best configuration for your needs
"""

import os
import sys
import configparser

def create_quick_config(preset="balanced", share_dir=None):
    """Create a quick configuration file"""
    if share_dir is None:
        share_dir = os.path.join(os.path.dirname(__file__), "index")
    
    config = configparser.ConfigParser()
    
    # Set up configuration based on preset
    if preset == "maximum":
        chunk_mb = 8
        socket_mb = 4
        workers = 6
        connections = 1500
    elif preset == "conservative":
        chunk_mb = 1
        socket_mb = 1
        workers = 2
        connections = 500
    else:  # balanced
        chunk_mb = 4
        socket_mb = 2
        workers = 4
        connections = 1000
    
    config['BASIC_SETTINGS'] = {
        'SHARE_DIR': share_dir,
        'PORT': '8000',
        'HOST': '0.0.0.0'
    }
    
    config['SPEED_PRESETS'] = {
        'PRESET': preset
    }
    
    config['PERFORMANCE_MANUAL'] = {
        'CHUNK_SIZE_MB': str(chunk_mb),
        'SOCKET_BUFFER_MB': str(socket_mb),
        'MAX_FILE_SIZE_GB': '16'
    }
    
    config['SERVER_MODE'] = {
        'USE_PRODUCTION': 'False',
        'WORKER_COUNT': str(workers),
        'WORKER_CONNECTIONS': str(connections),
        'ENABLE_THREADING': 'True'
    }
    
    config['FEATURES'] = {
        'ENABLE_RESUME': 'True',
        'ENABLE_CACHE': 'True',
        'CACHE_HOURS': '1',
        'UI_STYLE': 'professional',
        'SHOW_FILE_DETAILS': 'True'
    }
    
    config['ADVANCED'] = {
        'DEBUG_MODE': 'False',
        'CONNECTION_TIMEOUT': '120'
    }
    
    config_path = os.path.join(os.path.dirname(__file__), 'server_config.ini')
    with open(config_path, 'w') as f:
        config.write(f)
    
    print(f"✅ Created configuration: {config_path}")
    print(f"🎛️ Preset: {preset.upper()}")
    print(f"📁 Share directory: {share_dir}")
    return config_path

def main():
    print("🚀 Unified File Server - Quick Start")
    print("=" * 50)
    
    # Check for existing config
    config_path = os.path.join(os.path.dirname(__file__), 'server_config.ini')
    
    if len(sys.argv) > 1:
        preset = sys.argv[1].lower()
        if preset not in ["maximum", "balanced", "conservative"]:
            print("❌ Invalid preset. Use: maximum, balanced, or conservative")
            return
    else:
        if os.path.exists(config_path):
            print("📄 Found existing server_config.ini")
            response = input("Use existing config? (y/n): ").lower()
            if response.startswith('n'):
                preset = input("Choose preset (maximum/balanced/conservative): ").lower() or "balanced"
                create_quick_config(preset)
        else:
            print("🔧 No configuration found. Creating default...")
            preset = "balanced"
            create_quick_config(preset)
    
    # Import and run the server
    try:
        print("\n🔄 Starting server...")
        import server_config_driven
    except ImportError:
        print("❌ Could not import server_config_driven.py")
        print("Make sure server_config_driven.py is in the same directory")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()