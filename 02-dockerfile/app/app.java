package com.example;

import java.util.Random;
import java.text.DecimalFormat;

public class App {

    public static void main(String[] args) {

        System.out.println("Website Traffic Analytics Report");
        System.out.println("================================");

        int numberOfSessions = 100;

        double[] sessionDurations = generateSessionDurations(numberOfSessions);

        double mean = calculateMean(sessionDurations);

        double stdPopulation = calculateStandardDeviationPopulation(sessionDurations, mean);

        double stdSample = calculateStandardDeviationSample(sessionDurations, mean);

        DecimalFormat df = new DecimalFormat("#.##");

        System.out.println("Количество сессий: " + numberOfSessions);
        System.out.println("Средняя длительность сессии (сек): " + df.format(mean));
        System.out.println("Стандартное отклонение (генеральная совокупность): " + df.format(stdPopulation));
        System.out.println("Стандартное отклонение (выборка): " + df.format(stdSample));
    }

    private static double[] generateSessionDurations(int size) {

        Random random = new Random();
        double[] durations = new double[size];

        double min = 15.0;
        double max = 900.0;

        for (int i = 0; i < size; i++) {
            durations[i] = min + (max - min) * random.nextDouble();
        }

        return durations;
    }

    private static double calculateMean(double[] data) {

        double sum = 0.0;

        for (int i = 0; i < data.length; i++) {
            sum += data[i];
        }

        return sum / data.length;
    }

    private static double calculateStandardDeviationPopulation(double[] data, double mean) {

        double sumSquaredDifferences = 0.0;

        for (int i = 0; i < data.length; i++) {
            sumSquaredDifferences += Math.pow(data[i] - mean, 2);
        }

        double variance = sumSquaredDifferences / data.length;

        return Math.sqrt(variance);
    }

    private static double calculateStandardDeviationSample(double[] data, double mean) {

        double sumSquaredDifferences = 0.0;

        for (int i = 0; i < data.length; i++) {
            sumSquaredDifferences += Math.pow(data[i] - mean, 2);
        }

        double variance = sumSquaredDifferences / (data.length - 1);

        return Math.sqrt(variance);
    }
}
