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
//import java.util.List;
import java.util.Map;

@RestController
@Repository
public class JdbcZotdetectorRepository implements ZotdetectorRepository {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    // --------------------------------------------------------
    // Data ingestion endpoints
    // --------------------------------------------------------
    // Ingest Student data into SQL database
    @RequestMapping(
            value = "/api/data/student",
            method = RequestMethod.POST
    )
    @Override
    public Map<String, Boolean> addStudent(@RequestBody Map<String, Object> payload) {
        Integer id = (Integer) payload.get("id");
        String[] name = ((String) payload.get("name")).split(" ");
        String email = (String) payload.get("email");

        this.jdbcTemplate.update(
                "INSERT INTO Student(student_id, email, name_first, name_last) VALUES(?, ?, ?, ?)",
                id, email, name[0], name[1]
            );
        Map<String, Boolean> json = new HashMap<String, Boolean>();
        json.put("sucess", true);
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
    public Student getStudent(@RequestParam(required = false) Integer studentId) {
        String sql = "SELECT student_id, email, name_first, name_last " +
                "FROM Student " +
                "WHERE student_id = ?";
        return jdbcTemplate.query(connection -> {
            PreparedStatement stmt = connection.prepareStatement(sql);
            stmt.setInt(1, studentId);
            return stmt;
        }, resultSet -> {
            if (resultSet.next()) {
                return new Student(resultSet.getInt("student_id"), resultSet.getString("name_first"),
                        resultSet.getString("name_last"), resultSet.getString("email"));
            }
            return new Student(-1, "", "", "");
        });
    }
}