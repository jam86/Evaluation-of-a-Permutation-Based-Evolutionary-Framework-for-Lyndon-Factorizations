import java.io.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class Main {

    public static void main(String args[]) {
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

        if (args.length > 0 && (args[0].equals("order") || args[0].equals("graph"))) {
            //Map<String, String> sequence = new ReadFastaToString().read(args[2]);
            File file = new File(args[2]);
            BufferedReader reader = null;
            try {
                reader = new BufferedReader(new FileReader(file));
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
            HashMap<String, String> sequence = FastaHelper.fastaToMap(reader);
            String ordering = args[1];
            if (args[0].equals("graph")) {
                PartialOrder order = new PartialOrder(true);
                ArrayList<ModifiedDuval.ModCharacter> chars = order.fromString(args[1]);
                Collections.sort(chars, Collections.reverseOrder());
                StringBuilder sb = new StringBuilder();
                for (ModifiedDuval.ModCharacter c : chars) {
                    sb.append(c.getaChar());
                }
                ordering = sb.toString();
            }

            for (Map.Entry<String, String> entry : sequence.entrySet()) {
                System.out.println((new Duval()).factor(ordering.toCharArray(), entry.getValue().toCharArray()));
            }
        } else {
            Duval duval = null;
            if (printFactorsAndOrder) {
                duval = new Duval();
            }
            PartialOrder partialOrder;
            boolean nucleotideSequence = args[0].endsWith(".fna");
            //Map<String, String> sequence = new ReadFastaToString().read(args[0]);
            File file = new File(args[0]);
            BufferedReader reader = null;
            try {
                reader = new BufferedReader(new FileReader(file));
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
            HashMap<String, String> sequence;
            if (noFasta) {
                sequence = new HashMap<>();
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

                sequence.put(args[0], sb.toString());
            } else {
                sequence = FastaHelper.fastaToMap(reader);
            }
            for (Map.Entry<String, String> entry : sequence.entrySet()) {
                PartialOrder order = new PartialOrder(true);
                ArrayList<ModifiedDuval.ModCharacter> ordering = ModifiedDuval.factor(entry.getValue(), order, nucleotideSequence);
                if (printFactorsAndOrder) {
                    ArrayList<String> factors = duval.factor(order.toString().toCharArray(), entry.getValue().toCharArray());
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
                    System.out.println(entry.getKey() + "\0" + order.toString() + "\0" + factorOutput);
                } else {
                    System.out.println(entry.getKey() + "\0" + order.toString());
                }
            }
        }
    }
}
