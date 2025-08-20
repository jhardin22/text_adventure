"""
Configuration management for the text adventure game.
Handles loading, validation, and providing fallback values for game settings.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field


@dataclass
class ValidationError:
    """Represents a configuration validation error."""
    path: str
    message: str
    value: Any = None


class ConfigurationError(Exception):
    """Raised when configuration is invalid or cannot be loaded."""
    def __init__(self, message: str, errors: Optional[List[ValidationError]] = None):
        super().__init__(message)
        self.errors = errors or []


class ConfigLoader:
    """
    Manages loading and validation of game configuration.
    Provides fallback values and validates configuration integrity.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the config loader with optional custom path."""
        self.config_path = Path(config_path) if config_path else Path("data/config.json")
        self._config: Dict[str, Any] = {}
        self._validation_errors: List[ValidationError] = []
        
    def load(self) -> Dict[str, Any]:
        """
        Load configuration from file with validation and fallbacks.
        
        Returns:
            Dictionary containing the validated configuration.
            
        Raises:
            ConfigurationError: If critical validation errors are found.
        """
        # Start with default configuration
        self._config = self._get_default_config()
        
        # Try to load user configuration
        if self.config_path.exists():
            try:
                user_config = self._load_config_file()
                self._merge_configs(self._config, user_config)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Warning: Could not load config file: {e}")
                print("Using default configuration.")
        else:
            print(f"Config file not found at {self.config_path}. Using defaults.")
            
        # Validate the merged configuration
        self._validate_config()
        
        # Check if we have critical errors
        critical_errors = [e for e in self._validation_errors 
                          if "critical" in e.message.lower() or "required" in e.message.lower()]
        
        if critical_errors:
            raise ConfigurationError(
                "Critical configuration errors found", 
                critical_errors
            )
            
        # Log non-critical warnings
        for error in self._validation_errors:
            if error not in critical_errors:
                print(f"Config Warning: {error.path}: {error.message}")
                
        return self._config
    
    def _load_config_file(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> None:
        """
        Recursively merge override config into base config.
        Override values take precedence, but missing keys use base defaults.
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_configs(base[key], value)
            else:
                base[key] = value
    
    def _validate_config(self) -> None:
        """Validate the loaded configuration and collect errors."""
        self._validation_errors.clear()
        
        # Validate file paths
        self._validate_file_paths()
        
        # Validate text formatting options
        self._validate_text_formatting()
        
        # Validate gameplay settings
        self._validate_gameplay_settings()
        
        # Validate display settings
        self._validate_display_settings()
    
    def _validate_file_paths(self) -> None:
        """Validate file path configuration."""
        file_paths = self._config.get("file_paths", {})
        
        # Required paths
        required_paths = ["items_data", "rooms_data"]
        for path_key in required_paths:
            if path_key not in file_paths:
                self._validation_errors.append(
                    ValidationError(f"file_paths.{path_key}", "Critical: Required path missing")
                )
                continue
                
            path = Path(file_paths[path_key])
            if path_key == "rooms_data":
                # Rooms data should be a directory
                if not path.is_dir() and not path.exists():
                    self._validation_errors.append(
                        ValidationError(f"file_paths.{path_key}", f"Directory not found: {path}")
                    )
            else:
                # Other paths should be files
                if not path.exists():
                    self._validation_errors.append(
                        ValidationError(f"file_paths.{path_key}", f"File not found: {path}")
                    )
    
    def _validate_text_formatting(self) -> None:
        """Validate text formatting configuration."""
        formatting = self._config.get("text_formatting", {})
        
        # Validate numeric values
        numeric_fields = {
            "line_width": (40, 120),
            "paragraph_spacing": (0, 5),
            "separator_length": (10, 80)
        }
        
        for field, (min_val, max_val) in numeric_fields.items():
            if field in formatting:
                value = formatting[field]
                if not isinstance(value, int) or not (min_val <= value <= max_val):
                    self._validation_errors.append(
                        ValidationError(
                            f"text_formatting.{field}", 
                            f"Must be integer between {min_val} and {max_val}",
                            value
                        )
                    )
        
        # Validate color settings if colors are enabled
        if formatting.get("color_enabled", False):
            colors = formatting.get("colors", {})
            valid_colors = {"black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"}
            
            for color_key, color_value in colors.items():
                if color_value not in valid_colors:
                    self._validation_errors.append(
                        ValidationError(
                            f"text_formatting.colors.{color_key}",
                            f"Invalid color '{color_value}'. Valid colors: {', '.join(valid_colors)}",
                            color_value
                        )
                    )
    
    def _validate_gameplay_settings(self) -> None:
        """Validate gameplay configuration."""
        gameplay = self._config.get("gameplay", {})
        
        # Validate max inventory items
        max_items = gameplay.get("max_inventory_items")
        if max_items is not None:
            if not isinstance(max_items, int) or max_items < 1 or max_items > 100:
                self._validation_errors.append(
                    ValidationError(
                        "gameplay.max_inventory_items",
                        "Must be integer between 1 and 100",
                        max_items
                    )
                )
    
    def _validate_display_settings(self) -> None:
        """Validate display configuration."""
        display = self._config.get("display", {})
        
        # All display settings should be boolean
        boolean_fields = [
            "clear_screen_on_room_change", "show_room_name_on_look", 
            "show_exit_list", "verbose_descriptions", "show_item_count_in_inventory"
        ]
        
        for field in boolean_fields:
            if field in display and not isinstance(display[field], bool):
                self._validation_errors.append(
                    ValidationError(
                        f"display.{field}",
                        "Must be boolean (true/false)",
                        display[field]
                    )
                )
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration as fallback."""
        return {
            "file_paths": {
                "items_data": "data/items.json",
                "rooms_data": "data/rooms",
                "save_directory": "saves",
                "schemas_directory": "schemas"
            },
            "text_formatting": {
                "line_width": 80,
                "paragraph_spacing": 1,
                "choice_prefix": "  ",
                "choice_bullet": "•",
                "prompt_symbol": "> ",
                "separator_char": "-",
                "separator_length": 40,
                "color_enabled": False,
                "colors": {
                    "description": "white",
                    "choices": "cyan", 
                    "error": "red",
                    "success": "green",
                    "warning": "yellow",
                    "dog_text": "blue"
                }
            },
            "gameplay": {
                "max_inventory_items": 10,
                "auto_save": True,
                "save_on_room_change": True,
                "hint_system_enabled": True,
                "command_history_size": 50
            },
            "display": {
                "clear_screen_on_room_change": False,
                "show_room_name_on_look": True,
                "show_exit_list": True,
                "verbose_descriptions": True,
                "show_item_count_in_inventory": True
            },
            "debug": {
                "enabled": False,
                "log_commands": False,
                "log_state_changes": False,
                "show_room_ids": False
            },
            "version": "1.0.0"
        }

    def get(self, path: str, default: Any = None) -> Any:
        """
        Get a configuration value by dot-notation path.
        
        Args:
            path: Dot-separated path to the config value (e.g., "text_formatting.line_width")
            default: Default value if path not found
            
        Returns:
            The configuration value or default
        """
        keys = path.split('.')
        current = self._config
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
                
        return current