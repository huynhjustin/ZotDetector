package com.zotdetector;

public class Student {
    private int id;
    private String firstName;
    private String lastName;
    private String email;

    public Student(int id, String firstName, String lastName, String email) {
        this.id = id;
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
    }

    public int getId() { return this.id; }

    public String getFirstName() { return this.firstName; }

    public String getLastName() { return this.lastName; }

    public String getName() { return this.firstName + " " + this.lastName; }

    public String getEmail() { return this.email; }

    public String toString() {
        return "Strudent{" +
                "id='" + Integer.toString(this.id) + '\'' +
                ", firstName='" + this.firstName + '\'' +
                ", lastName=" + this.lastName +
                ", email='" + this.email + '\'' +
                '}';
    }
}