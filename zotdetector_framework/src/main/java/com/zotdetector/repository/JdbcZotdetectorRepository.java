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
        Map<String, Object> json = new HashMap<String, Object>();
        json.put("sucess", true);
        json.put("id", id);
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
        String sql = "DECLARE @StartDate DATE = CURDATE() " +
                "SELECT date, emotion, amount " +
                "FROM TrackDay " +
                "WHERE id = ? AND BETWEEN @StartDate AND DATEADD(DAY, ?, @StartDate)";
        return jdbcTemplate.query(connection -> {
            PreparedStatement stmt = connection.prepareStatement(sql);
            stmt.setString(1, id);
            stmt.setInt(2, duration * -1)
            return stmt;
        }, (resultSet, i) -> new EmotionDay(id, resultSet.getString("emotion"),
                resultSet.getDouble("amount"), resultSet.getString("date")));
    }
}