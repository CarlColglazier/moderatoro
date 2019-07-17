package main

import (
	"fmt"
	"github.com/bwmarrin/discordgo"
	"github.com/turnage/graw"
	"github.com/turnage/graw/reddit"
	"gopkg.in/yaml.v2"
	"io/ioutil"
	"log"
	"time"
)

type moderatoroBot struct {
	Bot        reddit.Bot
	Discord    *discordgo.Session
	Channel    string
	GrawConfig graw.Config
}

type ConfigValues struct {
	Subreddits     []string `yaml:"subreddits"`
	DiscordToken   string   `yaml:"discord_token"`
	DiscordChannel string   `yaml:"discord_channel"`
}

func InitBot() (*moderatoroBot, error) {
	bot, err := reddit.NewBotFromAgentFile(".agent", time.Duration(5)*time.Second)
	if err != nil {
		return nil, err
	}
	config := ConfigValues{}
	dat, _ := ioutil.ReadFile("config.yml")
	err = yaml.Unmarshal(dat, &config)
	if err != nil {
		log.Fatal(err)
	}
	session, err := discordgo.New(fmt.Sprintf("Bot %s", config.DiscordToken))
	if err != nil {
		return nil, err
	}
	cfg := graw.Config{Subreddits: config.Subreddits}
	handler := &moderatoroBot{
		Bot:        bot,
		Discord:    session,
		Channel:    config.DiscordChannel,
		GrawConfig: cfg,
	}
	return handler, nil
}

func (r *moderatoroBot) Post(p *reddit.Post) error {
	s := fmt.Sprintf("%s <https://redd.it/%s>", p.Title, p.ID)
	_, err := r.Discord.ChannelMessageSend(r.Channel, s)
	if err != nil {
		log.Println(err, s, r)
	}
	return nil
}

func main() {
	h, err := InitBot()
	if err != nil {
		log.Fatal(err)
	}
	if _, wait, err := graw.Run(h, h.Bot, h.GrawConfig); err != nil {
		fmt.Println("Failed: ", err)
	} else {
		fmt.Println("waiting")
		wait()
	}
}
