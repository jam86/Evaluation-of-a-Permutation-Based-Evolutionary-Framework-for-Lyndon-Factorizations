import java.io.*;
import java.util.*;

public class Main {
    public void run(String args[]) {
        boolean noFasta = false;
        boolean printFactorsAndOrder = false;
        boolean printFactorLengths = false;

        for(String arg : args) {
            if (arg.equals("noFasta")) {
                noFasta = true;
            }

            if (arg.equals("printFactorsAndOrder")) {
                printFactorsAndOrder = true;
            }

            if (arg.equals("printFactorLengths")) {
                printFactorLengths = true;
            }
        }

        HashMap<String, String> fasta = null;
        if (noFasta) {
            fasta = new HashMap<>();
            File file = new File(args[0]);
            BufferedReader reader = null;
            try {
                reader = new BufferedReader(new FileReader(file));
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }

            StringBuilder sb = new StringBuilder();
            String read;

            try {
                while ((read = reader.readLine()) != null) {
                    sb.append(read);
                    sb.append("\n");
                }
            } catch (IOException e) {
                e.printStackTrace();
            }

            fasta.put(args[0], sb.toString());
        } else {
            try {
                fasta = FastaHelper.fastaToMap(args[0]);
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
        }

        Duval duval = new Duval();
        for (Map.Entry<String, String> entry : fasta.entrySet()) {
            HashSet<Character> alphabet = new HashSet<>();
            for (char c : entry.getValue().toCharArray()) {
                alphabet.add(c);
            }
            /**
             * We need to make an alphabet ordering in the same order as the roman alphabet
             * so just sort the characters we find in the sequence.
             */
            ArrayList<Character> ordering = new ArrayList<>(alphabet);
            Collections.sort(ordering);
            char[] orderingArray = new char[ordering.size()];
            for(int i = 0; i < ordering.size(); i++) {
                orderingArray[i] = ordering.get(i);
            }

            ArrayList<String> factors = duval.factor(orderingArray, entry.getValue().toCharArray());
            if (printFactorsAndOrder) {
                String factorOutput;
                if (printFactorLengths) {
                    ArrayList<Integer> lengths = new ArrayList<>();
                    for (String factor : factors) {
                        lengths.add(factor.length());
                    }
                    factorOutput = lengths.toString();
                } else {
                    factorOutput = factors.toString();
                }
                System.out.println(entry.getKey() + "\0" + factors.toString() + "\0" + factorOutput);
            } else {
                System.out.println(entry.getKey() + "\0" + factors.toString());
            }
        }
    }

    public static void main(String args[]) {
        (new Main()).run(args);
    }
}
