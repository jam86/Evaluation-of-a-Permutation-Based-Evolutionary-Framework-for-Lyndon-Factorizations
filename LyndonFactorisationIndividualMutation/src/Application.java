import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.lang.reflect.InvocationTargetException;
import java.util.*;

import org.apache.commons.math3.distribution.PoissonDistribution;
import org.apache.commons.math3.util.Pair;


public class Application {
    public static void main(String[] args) {
        (new Application()).run(args);
    }

    Duval duval = new Duval();
    String text = "";
    HashSet<Character> alphabet;
    Random random = new Random();
    boolean useRLEFitness = false;
    boolean usePopulation = false;

    private void run(String[] args) {
        Mutation mutation = null;
        int mutationCount = 1;
        boolean differenceOnly = false;
        PoissonDistribution poissonDist = new PoissonDistribution(1);

        alphabet = new HashSet<>();
        for(char c : text.toCharArray()) {
            alphabet.add(c);
        }

        if (args.length != 0) {
            useRLEFitness = (args.length >= 3 && args[2].equals("1"));
            usePopulation = (args.length >= 4 && args[3].equals("1"));

            Integer arg = Integer.parseInt(args[0]);
            switch (arg) {
                case -1: {
                    runCombineOperators();
                    return;
                }
                case 0: {
                    // swap mutation
                    mutation = new SwapMutation();
                    mutationCount = 1;
                    break;
                }
                case 1: {
                    // swap mutation with 3 mutations
                    mutation = new SwapMutation();
                    mutationCount = 3;
                    break;
                }
                case 2: {
                    // scramble mutation
                    mutation = new ScrambleMutation();
                    mutationCount = 1;
                    break;
                }
                case 3: {
                    // scramble mutation with 3 mutations
                    mutation = new ScrambleMutation();
                    mutationCount = 3;
                    break;
                }
                case 4: {
                    // insertion mutation
                    mutation = new InsertionMutation();
                    mutationCount = 1;
                    break;
                }
                case 5: {
                    // insertion mutation with 3 mutations
                    mutation = new InsertionMutation();
                    mutationCount = 3;
                    break;
                }
                case 6: {
                    mutation = new ModifiedDuvalsMutation(text);
                    mutationCount = 1;
                    break;
                }
                case 7: {
                    mutation = new ModifiedDuvalsMutation(text);
                    mutationCount = 3;
                    break;
                }
                case 8: {
                    mutation = new SwapMutation();
                    mutationCount = poissonDist.sample() + 1;
                    break;
                }
                case 9: {
                    mutation = new ScrambleMutation();
                    mutationCount = poissonDist.sample() + 1;
                    break;
                }
                case 10: {
                    mutation = new InsertionMutation();
                    mutationCount = poissonDist.sample() + 1;
                    break;
                }
                case 11: {
                    mutation = new ModifiedDuvalsMutation(text);
                    mutationCount = poissonDist.sample() + 1;
                    break;
                }
                default: {
                    System.err.println("Missing experiment number");
                    System.err.println(arg);
                    return;
                }
            }

            if (args.length != 1) {
                differenceOnly = (args[1].equals("1"));
            }
        } else {
            System.err.println("Usage: [experiment number] [output difference only 0/1 (optional)] " +
                    "[use RLE size as fitness 0/1 (optional)] [use a population 0/1 (optional)] " +
                    "[population method crossover operator (optional)] [fasta file to use as input (optional)] " +
                    "[use max / min factor length difference as fitness (optional)] [use min factor count fitness] " +
                    "[use stdev fitness func (optional)]");
            return;
        }



        boolean useMaxMinDiffFitness = args.length >= 7 && args[6].equals("1");
        boolean useMinFactorCountFitness = args.length >= 9 && args[8].equals("1");

        if (useMaxMinDiffFitness) {
            runMaxMinDiffFitnessAnalyseOperator(mutation, mutationCount, args);
            return;
        } else if (useMinFactorCountFitness) {
            runMinFactorCountFitnessAnalyseOperator(mutation, mutationCount, args);
            return;
        }

        if (differenceOnly) {
            runOperatorDifference(mutation, mutationCount);
        } else {
            runAnalyseOperator(mutation, mutationCount);
        }
    }

    private void runMinFactorCountFitnessAnalyseOperator(Mutation mutation, int mutationCount, String[] args) {
        boolean useSimulatedAnnealing = args.length >= 8 && args[7].equals("1");

        File file = new File(args[5]);
        BufferedReader reader = null;
        try {
            reader = new BufferedReader(new FileReader(file));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        HashMap<String, String> fasta = FastaHelper.fastaToMap(reader);
        for (Map.Entry<String, String> entry : fasta.entrySet()) {
            System.out.println(">" + entry.getKey());
            HashSet<Character> alphabet = new HashSet<>();
            for (char c : entry.getValue().toCharArray()) {
                alphabet.add(c);
            }

            if (mutation instanceof ModifiedDuvalsMutation) {
                mutation = new ModifiedDuvalsMutation(entry.getValue());
            }
            ArrayList<Character> newOrdering;
            ArrayList<Character> ordering = new ArrayList<>(alphabet);
            Collections.shuffle(ordering, new Random());
            int prevFitness = 999999999;
            int currentDifference = 0;
            for (int i = 0; i < 3000; i++) {
                if (prevFitness == 1) {
                    System.out.printf("%s:%d:%d%n", ordering.toString(), currentDifference, prevFitness);
                    continue;
                }
                newOrdering = (ArrayList<Character>) ordering.clone();
                for (int j = 0; j < mutationCount; j++) {
                    newOrdering = mutation.mutate(newOrdering);
                }

                //ArrayList<String> factors = duval.factor(newOrdering.toString().toCharArray(), text.toCharArray());
                int fitness = getFitness(newOrdering);

                currentDifference = (prevFitness - fitness);
                if (prevFitness >= fitness) {
                    prevFitness = fitness;
                    ordering = newOrdering;
                } else if (0.5 >= (random.nextDouble() % 1) && useSimulatedAnnealing) {
                    prevFitness = fitness;
                    ordering = newOrdering;
                }

                System.out.printf("%s:%d:%d%n", ordering.toString(), currentDifference, prevFitness);
            }
        }
    }

    private void runMaxMinDiffFitnessAnalyseOperator(Mutation mutation, int mutationCount, String[] args) {
        boolean useSimulatedAnnealing = args.length >= 8 && args[7].equals("1");
        boolean useStdevFitness = args.length >= 10 && args[9].equals("1");

        File file = new File(args[5]);
        BufferedReader reader = null;
        try {
            reader = new BufferedReader(new FileReader(file));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        HashMap<String, String> fasta = FastaHelper.fastaToMap(reader);
        for (Map.Entry<String, String> entry : fasta.entrySet()) {
            System.out.println(">" + entry.getKey());
            HashSet<Character> alphabet = new HashSet<>();
            for (char c : entry.getValue().toCharArray()) {
                alphabet.add(c);
            }

            if (mutation instanceof ModifiedDuvalsMutation) {
                mutation = new ModifiedDuvalsMutation(entry.getValue());
            }
            //final int initialFitnessValue = 999999999;
            double currentDifference = 0;
            ArrayList<Character> ordering = new ArrayList<>(alphabet);
            Collections.shuffle(ordering, new Random());
            ArrayList<Integer> factorLengths = null;
            double prevFitness = 0;
            Pair ret;
            if (useStdevFitness) {
                ret = getFitnessStdevFactors(ordering, entry.getValue());
            } else {
                ret = getFitnessMaxMinFactorLengthDifference(ordering, entry.getValue());
            }
            prevFitness = (double) ret.getFirst();
            factorLengths = (ArrayList<Integer>) ret.getSecond();
            ArrayList<Character> newOrdering;
            // we find the plateau for without SA or fixed accept for diff mutation to be 60000
            // and for stdev fitness to be 100000
            // but we use 10000 since the improvement for both fitness is not very much after then
            final int maxIters = 10000; //(useStdevFitness? 20000:60000);
            final double initialTemperature = 200;
            double temperature = initialTemperature;
            final double temperatureLowerBound = 10;
            int timesNotImproved = 0;
            int timesKeptWorse = 0;
            for(int i = 0; i < maxIters; i++) {
                if (useStdevFitness) {
                    if (prevFitness == 0) {
                        continue;
                    }
                } else {
                    if (prevFitness == 0) {
                        continue;
                    }
                }

                newOrdering = (ArrayList<Character>) ordering.clone();
                for (int j = 0; j < mutationCount; j++) {
                    newOrdering = mutation.mutate(newOrdering);
                }

                double fitness;
                if (useStdevFitness) {
                    ret = getFitnessStdevFactors(newOrdering, entry.getValue());
                } else {
                    ret = getFitnessMaxMinFactorLengthDifference(newOrdering, entry.getValue());
                }
                fitness = (double) ret.getFirst();
                factorLengths = (ArrayList<Integer>) ret.getSecond();

                currentDifference = (prevFitness - fitness);
                if (prevFitness >= fitness) {
                    if (prevFitness == fitness) {
                        timesNotImproved += 1;
                    } else {
                        timesNotImproved = 0;
                    }

                    prevFitness = fitness;
                    ordering = newOrdering;
                    /*Math.exp(currentDifference / temperature)*/
                } else if (0.1 >= (random.nextDouble() % 1) && useSimulatedAnnealing && fitness != 999999999) {
                    prevFitness = fitness;
                    ordering = newOrdering;
                    timesKeptWorse += 1;
                }
                /*} else {
                    timesNotImproved += 1;
                }*/

                /*if (useSimulatedAnnealing) {
                    if (timesNotImproved >= 25) {
                        timesNotImproved = 0;

                        // we need to print and continue here so that the values printed do not include big spikes of
                        // initial fitness values
                        System.out.printf("%s:%d:%d%n", ordering.toString(), currentDifference, prevFitness);
                        //boolean firstRun = true;
                        //while(prevFitness - fitness <= -50 || firstRun) {
                        //    firstRun = false;
                            Collections.shuffle(ordering, new Random());
                            fitness = getFitnessMaxMinFactorLengthDifference(ordering, entry.getValue());
                        //}
                        prevFitness = fitness;
                        continue;
                    }

                }*/

                System.out.printf("%s:%f:%f:%s%n", ordering.toString(), currentDifference, prevFitness, factorLengths);
                //System.out.println(new Duval().factor(ordering, entry.getValue().toCharArray()));
                // log 0 is undefined and log 1 is 0
                //temperature -= 1.0 / Math.log(i + 2);
                /*temperature -= initialTemperature / (float)maxIters;

                if (temperature < temperatureLowerBound) {
                    temperature = temperatureLowerBound;
                }*/
            }
            //System.out.println(new Duval().factor(ordering, entry.getValue().toCharArray()));
            //System.out.println(timesKeptWorse);
        }
    }

    private Pair<Double, ArrayList<Integer>> getFitnessMaxMinFactorLengthDifference(ArrayList<Character> ordering, String text) {
        ArrayList<String> factors = duval.factor(ordering, text.toCharArray());
        ArrayList<Integer> factorLengths = new ArrayList<>();

        if (factors.size() == 1) {
            factorLengths.add(factors.get(0).length());
            return Pair.create(999999999.0, new ArrayList());
        }

        int minFactorLen = 999999999, maxFactorLen = 0;
        for (String factor:factors) {
            int length = factor.length();
            factorLengths.add(length);
            if (length > maxFactorLen) {
                maxFactorLen = length;
            }

            if (length < minFactorLen) {
                minFactorLen = length;
            }
        }

        return Pair.create((double)(maxFactorLen - minFactorLen), factorLengths);
    }

    private Pair<Double, ArrayList<Integer>> getFitnessStdevFactors(ArrayList<Character> ordering, String text) {
        ArrayList<String> factors = duval.factor(ordering, text.toCharArray());
        ArrayList<Integer> factorLengths = new ArrayList<>();

        if (factors.size() == 1) {
            factorLengths.add(factors.get(0).length());
            return Pair.create(999999999.0, new ArrayList());
        }

        double mean = 0;
        for (String factor:factors) {
            mean += factor.length();
            factorLengths.add(factor.length());
        }
        mean /= factors.size();

        double stdev = 0;
        for (String factor:factors) {
            stdev += Math.pow(mean - factor.length(), 2);
        }
        return Pair.create(stdev / factors.size(), factorLengths);
    }

    /**
     * Run a combination of operators with random chance to apply additional operators
     * Print the operator information, ordering, and fitness
     */
    private void runCombineOperators() {
        Class[] classes = {
                null,
                MultipleSwapMutation.class,
                MultipleInsertionMutation.class,
                MultipleScrambleMutation.class,
        };
        ArrayList<MultipleMutation> operators = new ArrayList<>();

        for (Class _class : classes) {
            try {
                for (Class _class2 : classes) {
                    for (Class _class3 : classes) {
                        MultipleMutation multipleMutationTop, multipleMutation2 = null, multipleMutation3 = null;

                        if (_class3 != null) {
                            multipleMutation3 = (MultipleMutation) _class3.getConstructor(MultipleMutation.class, double.class).newInstance(null, 0);
                        }

                        if (_class2 != null) {
                            multipleMutation2 = (MultipleMutation) _class2.getConstructor(MultipleMutation.class, double.class).newInstance(multipleMutation3, random.nextDouble() % 100);
                        }

                        if (_class != null) {
                            multipleMutationTop = (MultipleMutation) _class.getConstructor(MultipleMutation.class, double.class).newInstance(multipleMutation2, random.nextDouble() % 100);
                        } else {
                            // dont add null to the array of existing operators
                            continue;
                        }

                        operators.add(multipleMutationTop);
                    }
                }

            } catch (NoSuchMethodException | IllegalAccessException | InstantiationException | InvocationTargetException e) {
                e.printStackTrace();
            }
        }

        ArrayList<Character> ordering = new ArrayList<>(alphabet);
        for (MultipleMutation operator : operators) {
            ArrayList<Character> newOrdering;
            Collections.shuffle(ordering, new Random());
            int prevFitness = -99;
            int currentDifference = 0;
            for(int i = 0; i < 10000; i++) {
                newOrdering = (ArrayList<Character>) ordering.clone();
                for (int j = 0; j < 1; j++) {
                    newOrdering = operator.mutate(newOrdering);
                }

                //ArrayList<String> factors = duval.factor(newOrdering.toString().toCharArray(), text.toCharArray());
                int fitness = getFitness(ordering);

                if (fitness >= prevFitness) {
                    // plots have large -99 spikes in them so change -99 to 0
                    if (prevFitness == -99) {
                        prevFitness = 0;
                    }
                    currentDifference = (prevFitness - fitness);
                    prevFitness = fitness;
                    ordering = newOrdering;
                }

                System.out.printf("%s:%s:%s:%d:%d%n", operator.hashCode(), operator, ordering.toString(), currentDifference, prevFitness);
            }
        }
    }

    /**
     * For a set number of random iterations, mutate and get difference between
     * the new and current ordering
     * @param mutation
     * @param mutationCount
     */
    private void runOperatorDifference(Mutation mutation, int mutationCount) {
        ArrayList<Character> ordering = new ArrayList<>(alphabet);

        for (int i = 0; i < 200; i++) {
            Collections.shuffle(ordering, new Random());
            int prevFitness = getFitness(ordering);

            ArrayList<Character> newOrdering;
            for (int j = 0; j < 50000; j++) {
                newOrdering = (ArrayList<Character>) ordering.clone();
                for (int k = 0; k < mutationCount; k++) {
                    newOrdering = mutation.mutate(newOrdering);
                }

                int fitness = getFitness(newOrdering);

                System.out.println(prevFitness - fitness);
            }
        }
    }

    private int getFitness(ArrayList<Character> ordering) {
        return duval.factor(ordering, text.toCharArray()).size();
    }

    private void runAnalyseOperator(Mutation mutation, int mutationCount) {
        ArrayList<Character> ordering = new ArrayList<>(alphabet);
        ArrayList<Character> newOrdering;
        Collections.shuffle(ordering, new Random());
        int prevFitness = -99;
        int currentDifference = 0;
        for(int i = 0; i < 10000; i++) {
            newOrdering = (ArrayList<Character>) ordering.clone();
            for (int j = 0; j < mutationCount; j++) {
                newOrdering = mutation.mutate(newOrdering);
            }

            //ArrayList<String> factors = duval.factor(newOrdering.toString().toCharArray(), text.toCharArray());
            int fitness = getFitness(newOrdering);

            // plots have large -99 spikes in them so change -99 to 0
            if (prevFitness == -99) {
                prevFitness = 0;
            }
            currentDifference = (prevFitness - fitness);
            prevFitness = fitness;
            ordering = newOrdering;

            System.out.printf("%s:%d:%d%n", ordering.toString(), currentDifference, prevFitness);
        }
    }
}
