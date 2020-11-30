package com.zotdetector.repository;

import com.zotdetector.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.PreparedStatementCreator;
import org.springframework.jdbc.core.SqlOutParameter;
import org.springframework.jdbc.core.SqlParameter;
import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
import org.springframework.jdbc.core.namedparam.SqlParameterSource;
import org.springframework.jdbc.core.simple.SimpleJdbcCall;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.stereotype.Repository;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpSession;
import javax.sql.DataSource;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.*;
import java.text.SimpleDateFormat;
import java.util.Date;

@RestController
@Repository
public class JdbcZotdetectorRepository implements ZotdetectorRepository {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    // Collection of unique Student Ids
    HashSet<Integer> uniqueIds = new HashSet<Integer>();

    // --------------------------------------------------------
    // Data ingestion endpoints
    // --------------------------------------------------------
    // Ingest Student data into SQL database
    @RequestMapping(
            value = "/api/data/student",
            method = RequestMethod.POST
    )
    @Override
    public Map<String, Object> addStudent(@RequestBody Map<String, Object> payload) {
        Map<String, Object> json = new HashMap<String, Object>();
        try {
            String[] name = ((String) payload.get("name")).split(" ");
            String email = (String) payload.get("email");
            Random rand = new Random();
            Integer id = rand.nextInt(1000);
            while (uniqueIds.contains(id)) id = rand.nextInt(1000); // Keep getting random id until unique
            uniqueIds.add(id);

            this.jdbcTemplate.update(
                    "INSERT INTO Student(id, email, name_first, name_last) VALUES(?, ?, ?, ?)",
                    id, email, name[0], name[1]
            );
            json.put("success", true);
            json.put("id", id);
        } catch (Exception e) {
            json.put("success", false);
            json.put("message", e.getMessage());
        }
        return json;
    }

    // Ingest Student emotion data into SQL database
    @RequestMapping(
            value = "/api/data/emotion",
            method = RequestMethod.POST
    )
    @Override
    public Map<String, Object> addEmotion(@RequestBody Map<String, Object> payload) {
        Map<String, Object> json = new HashMap<String, Object>();
        // Verify if student id already exists
        Integer id = (Integer) payload.get("id");
        if (!uniqueIds.contains(id)) {
            json.put("success", false);
            json.put("message", "Student id does not exist");
            return json;
        }
        // Convert string into SQL Date object
        try {
            String date = (String) payload.get("date");
            // TODO get emotion and amount from DS side
            String emotion = "happy";
            Double amount = 0.5;

            // Upsert emotion data into SQL database
            // TODO calculate average emotion rather than overriding existing data
            this.jdbcTemplate.update(
                    "INSERT INTO TrackDay (date, id, emotion, amount) VALUES (?, ?, ?, ?) " +
                            "ON DUPLICATE KEY UPDATE emotion = ?, amount = ?",
                    date, id, emotion, amount, emotion, amount
            );
            json.put("success", true);
            json.put("id", id);
            json.put("date", date);
        } catch (Exception e) {
            json.put("success", false);
            json.put("message", e.getMessage());
        }
        return json;
    }

    // --------------------------------------------------------
    // Data retrieval endpoints
    // --------------------------------------------------------
    // Retrieve Student data from student id
    @RequestMapping(
            value = "api/ret/student",
            method = RequestMethod.GET
    )
    @Override
    public Student getStudent(@RequestParam(required = false) Integer id) {
        String sql = "SELECT id, email, name_first, name_last " +
                "FROM Student " +
                "WHERE id = ?";
        return jdbcTemplate.query(connection -> {
            PreparedStatement stmt = connection.prepareStatement(sql);
            stmt.setInt(1, id);
            return stmt;
        }, resultSet -> {
            Student s;
            if (resultSet.next()) {
                return new Student(resultSet.getInt("id"), resultSet.getString("name_first"),
                        resultSet.getString("name_last"), resultSet.getString("email"));
            }
            return new Student(-1, "", "", "");
        });
    }

    // Retrieve complete EmotionDay data from student id and duration
    @RequestMapping(
            value = "api/ret/allEmotions",
            method = RequestMethod.GET
    )
    @Override
    public List<EmotionDay> getEmotions(@RequestParam(required = false) Integer id, Integer duration) {
        String sql = "SELECT date, emotion, amount " +
                "FROM TrackDay " +
                "WHERE id = ? AND date >= ADDDATE(CURDATE(), ?)";
        return jdbcTemplate.query(connection -> {
            PreparedStatement stmt = connection.prepareStatement(sql);
            stmt.setInt(1, id);
            stmt.setInt(2, duration * -1);
            return stmt;
        }, (resultSet, i) -> new EmotionDay(id, resultSet.getString("emotion"),
                resultSet.getDouble("amount"), resultSet.getString("date")));
    }

    // --------------------------------------------------------
    // Database Admin endpoints - TAKE CAUTION BEFORE USING
    // --------------------------------------------------------
    // Delete ALL records in local SQL database
    @RequestMapping(
            value = "/api/deleteDatabase",
            method = RequestMethod.POST
    )
    @Override
    public Map<String, Object> deleteDatabase() {
        Map<String, Object> json = new HashMap<String, Object>();
        try {
            this.jdbcTemplate.update("DELETE FROM Student");
            json.put("success", true);
        } catch (Exception e) {
            json.put("success", false);
            json.put("message", e.getMessage());
        }
        return json;
    }
}