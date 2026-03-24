package com.analytics;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class App {
    public static void main(String[] args) {
        String csvFile = System.getenv("DATA_PATH");
        if (csvFile == null || csvFile.isEmpty()) {
            csvFile = "/data/traffic_data.csv";
        }
        String line = "";
        String cvsSplitBy = ",";
        List<Double> durations = new ArrayList<>();

        System.out.println("=== Website Traffic Analytics ===");
        System.out.println("Theme: Website Traffic (Variant 14)");
        System.out.println("Reading data from: " + csvFile);

        try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {
            // Skip header
            br.readLine();
            while ((line = br.readLine()) != null) {
                String[] record = line.split(cvsSplitBy);
                if (record.length >= 2) {
                    durations.add(Double.parseDouble(record[1]));
                }
            }
        } catch (IOException e) {
            System.err.println("Error reading CSV file: " + e.getMessage());
            System.err.println("Make sure the data volume is correctly mounted.");
            return;
        }

        if (durations.isEmpty()) {
            System.out.println("No data found in CSV.");
            return;
        }

        int n = durations.size();
        System.out.println("Processing " + n + " session records...");

        double sum = 0;
        for (double d : durations) {
            sum += d;
        }
        double mean = sum / n;

        double sqDiffSum = 0;
        for (double d : durations) {
            sqDiffSum += Math.pow(d - mean, 2);
        }
        double variance = sqDiffSum / n;
        double stdDev = Math.sqrt(variance);

        System.out.println("\n--- Results ---");
        System.out.printf("Average Session Duration: %.2f seconds\n", mean);
        System.out.printf("Standard Deviation: %.2f seconds\n", stdDev);
        System.out.println("----------------\n");

        if (stdDev > 200) {
            System.out.println("Insight: High variability in session durations detected.");
        } else {
            System.out.println("Insight: Session durations are relatively consistent.");
        }
    }
}
