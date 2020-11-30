package com.zotdetector;

enum Emotion {
    HAPPY, SAD, STRESSED;
}

public class EmotionDay {
    private int id;
    private Emotion emotion;
    private double amount;
    private String date;

    public EmotionDay(int id, String emotion, double amount, String date) {
        this.id = id;
        this.emotion = Emotion.valueOf(emotion.toUpperCase());
        this.amount = amount;
        this.date = date;
    }

    public int getId() { return this.id; }

    public Emotion getEmotion() { return this.emotion; }

    public Double getAmount() { return this.amount; }

    public String getDate() { return this.date; }

    public String toString() {
        return "EmotionDay{" +
                "id=" + Integer.toString(this.id) +
                ", emotion='" + this.emotion.toString() + '\'' +
                ", amount='" + Double.toString(this.amount) + '\'' +
                ", date='" + this.date + '\'' +
                '}';
    }
}