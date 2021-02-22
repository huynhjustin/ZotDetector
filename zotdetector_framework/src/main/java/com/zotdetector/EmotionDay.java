package com.zotdetector;

import java.util.HashMap;
import java.util.Map;

public class EmotionDay {
    private String date;
    private Double angry;
    private Double disgusted;
    private Double fearful;
    private Double happy;
    private Double neutral;
    private Double sad;
    private Double surprised;

    public EmotionDay(String date, Double angry, Double disgusted, Double fearful,
                      Double happy, Double neutral, Double sad, Double surprised) {
        this.date = date;
        this.angry = angry;
        this.disgusted = disgusted;
        this.fearful = fearful;
        this.happy = happy;
        this.neutral = neutral;
        this.sad = sad;
        this.surprised = surprised;
    }

    public String getDate() { return this.date; }

    public Map<String, Double> getEmotions() {
        Map<String, Double> emotions = new HashMap<String, Double>();
        emotions.put("angry", this.angry);
        emotions.put("disgusted", this.disgusted);
        emotions.put("fearful", this.fearful);
        emotions.put("happy", this.happy);
        emotions.put("neutral", this.neutral);
        emotions.put("sad", this.sad);
        emotions.put("surprised", this.surprised);
        return emotions;
    }

    public String toString() {
        return "EmotionDay{" +
                "date='" + this.date + '\'' +
                ", emotions= { angry='" + Double.toString(this.angry) + '\'' +
                ", disgusted='" + Double.toString(this.disgusted) + '\'' +
                ", fearful='" + Double.toString(this.fearful) + '\'' +
                ", happy='" + Double.toString(this.happy) + '\'' +
                ", neutral='" + Double.toString(this.neutral) + '\'' +
                ", sad='" + Double.toString(this.sad) + '\'' +
                ", surprised='" + Double.toString(this.surprised) + '\'' +
                "} }";
    }
}