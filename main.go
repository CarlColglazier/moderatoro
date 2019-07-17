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
	discord    *discordgo.Session
	channel    string
	GrawConfig graw.Config
}

type ConfigValues struct {
	Subreddits     []string `yaml:"subreddits"`
	DiscordToken   string   `yaml:"discord_token"`
	DiscordChannel string   `yaml:"discord_channel"`
}

func InitBot() (*moderatoroBot, error) {
	bot, err := reddit.NewBotFromAgentFile(".agent", time.Duration(60)*time.Second)
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
		discord:    session,
		channel:    config.DiscordChannel,
		GrawConfig: cfg,
	}
	return handler, nil
}

func (r *moderatoroBot) Post(p *reddit.Post) error {
	s := fmt.Sprintf("%s <https://redd.it/%s>", p.Title, p.ID)
	_, err := r.discord.ChannelMessageSend(r.channel, s)
	return err
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
