package com.zotdetector;

emun Emotion {HAPPY, SAD, STRESSED}

public class EmotionDay {
    private int id;
    private Emotion emotion;
    private double amount;
    private String date;

    public EmotionDay(int id, String emotion, double amount, String date) {
        this.id = id;
        this.emotion = this.stringToEmotion(emotion);
        this.amount = amount;
        this.date = date;
    }

    public int getId() { return this.id; }

    public Emotion getEmotion() { return this.emotion; }

    public Double getAmount() { return this.amount; }

    public String getDate() { return this.date; }

    public Emotion stringToEmotion(String emotion) {
        switch (emotion) {
            case "happy": return Emotion.HAPPY;
            case "sad": return Emotion.SAD;
            case "stressed": return Emotion.STRESSED;
        }
    }

    public String emotionToString() {
        switch (this.emotion) {
            case HAPPY: return "happy";
            case SAD: return "sad";
            case STRESSED: return "stressed";
        }
    }

    public String toString() {
        return "EmotionDay{" +
                "id=" + Integer.toString(this.id) +
                ", emotion='" + this.emotionToString() + '\'' +
                ", amount='" + Integer.toString(this.amount) + '\'' +
                ", date='" + this.date + '\'' +
                '}';
    }
}