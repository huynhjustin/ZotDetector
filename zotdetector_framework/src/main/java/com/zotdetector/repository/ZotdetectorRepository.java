package com.zotdetector.repository;

import com.zotdetector.*;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;

import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.sql.SQLException;
//import java.util.List;
import java.util.Map;

public interface ZotdetectorRepository {
    // --------------------------------------------------------
    // Data ingestion endpoints
    // --------------------------------------------------------
    /**
     * API handler for student data
     * /api/student[?name=xxx[&email=xxx]]
     *
     * @return
     */
    Map<String, Boolean> addStudent(Map<String, Object> payload);

    // --------------------------------------------------------
    // Data retrieval endpoints
    // --------------------------------------------------------

    /**
     * API handler for student data
     * /api/student
     *
     * @param studentId     Retrieve Student information that matches the specified id
     * @return              Student that matches the filter
     */
    Student getStudent(Integer studentId);
}
