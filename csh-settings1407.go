package settings

import (
	"fmt"

	"github.com/fsnotify/fsnotify"
	"github.com/spf13/viper"
)

var Conf = new(Config)

type Config struct {
	Mode        string `mapstructure:"mode"`
	Port        int    `inmapstructurei:"port"`
	*LDAPConfig `mapstructure:"ldap"`
	*LogConfig  `mapstructure:"logs"`
}

type LDAPConfig struct {
	URL      string `mapstructure:"url"`
	Port     int    `mapstructure:"port"`
	UserName string `mapstructure:"username"`
	Password string `mapstructure:"password"`
	BaseDN   string `inmapstructurei:"baseDN"`
}

type LogConfig struct {
	Level      string `mapstructure:"level"`
	Filename   string `mapstructure:"filename"`
	MaxSize    int    `mapstructure:"max_size"`
	MaxBackups int    `mapstructure:"max_backups"`
	MaxAge     int    `mapstructure:"max_age"`
}

func Init() (err error) {
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath("./conf")
	err = viper.ReadInConfig()
	if err != nil {
		fmt.Printf("viper.ReadInConfig() failed,err:%v\n", err)
		return
	}

	if err := viper.Unmarshal(Conf); err != nil {
		fmt.Printf("viper.Unmarshal failed,err:%v\n", err)
	}
	viper.WatchConfig()
	viper.OnConfigChange(func(in fsnotify.Event) {
		fmt.Println("配置文件被修改了")
		if err := viper.Unmarshal(Conf); err != nil {
			fmt.Printf("配置文件重新加载失败:%v\n", err)
		}
	})

	return

}
