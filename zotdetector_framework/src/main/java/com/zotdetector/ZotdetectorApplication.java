package com.zotdetector;

import com.zotdetector.repository.ZotdetectorRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.jdbc.core.JdbcTemplate;

import javax.servlet.http.HttpSession;

@SpringBootApplication
public class ZotdetectorApplication implements CommandLineRunner {
    private static final Logger log = LoggerFactory.getLogger(ZotdetectorApplication.class);

    @Autowired
    JdbcTemplate jdbcTemplate;

    @Autowired
    @Qualifier("jdbcZotdetectorRepository")
    private ZotdetectorRepository zotdetectorRepository;

    public static void main(String[] args) { SpringApplication.run(ZotdetectorApplication.class, args); }

    @Override
    public void run(String... args) { log.info("ZotdetectorApplication..."); }
}