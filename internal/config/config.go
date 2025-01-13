package config

import (
	"os"
	"path/filepath"
	"sync"
)

type Config struct {
	RootDir string `yaml:"root_dir"`
}

var instance *Config
var once sync.Once

// Creates a new config file
func Get() *Config {
	once.Do(func() {
		dir, _ := os.UserConfigDir()
		path := filepath.Join(dir, "pinkmess")
		instance = &Config{RootDir: path}
	})
	return instance
}
