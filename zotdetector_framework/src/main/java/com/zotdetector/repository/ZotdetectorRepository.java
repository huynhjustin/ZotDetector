package com.zotdetector.repository;

import com.zotdetector.*;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;

import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.sql.SQLException;
import java.util.Map;

public interface ZotdetectorRepository {
    // --------------------------------------------------------
    // Data ingestion endpoints
    // --------------------------------------------------------
    /**
     * API handler for student data
     * /api/data/student
     *
     * @return
     */
    Map<String, Object> addStudent(Map<String, Object> payload);

    /**
     * API handler for emotion data
     * /api/data/emotion
     *
     * @return
     */
    Map<String, Object> addEmotion(Map<String, Object> payload);

    // --------------------------------------------------------
    // Data retrieval endpoints
    // --------------------------------------------------------
    /**
     * API handler for student data
     * /api/ret/student[?id=xxx]
     *
     * @param id     Retrieve Student information that matches the specified id
     * @return       Student that matches the filter
     */
    Student getStudent(Integer id);

    /**
     * API handler for emotional data
     * /api/ret/allEmotions[?id=xxx[&duration=xxx]]
     *
     * @param id        Retrieve Emotion information that matches the specifed id
     * @param duration  Retrieve Emotion information within specifed duration
     * @return          List of EmotionDay that match the filters
     */
    List<EmotionDay> getEmotions(Integer id, Integer duration);
}
