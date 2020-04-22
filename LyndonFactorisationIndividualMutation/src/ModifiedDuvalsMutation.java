import java.util.ArrayList;
import java.util.Random;

/**
 * Mutation operator which works in the way that the modified duvals algorithm does
 * IE: if a factor would be created, change the ordering so that the algorithm would continue instead
 */
public class ModifiedDuvalsMutation implements Mutation {
    private Random random = new Random();
    private String text;

    public ModifiedDuvalsMutation(String text) {
        super();
        this.text = text;
    }

    public ArrayList<Character> mutate(ArrayList<Character> order) {
        Duval duval = new Duval();

        ArrayList<String> factors = duval.factor(order, text.toCharArray());
        if (factors.size() > 1) {
            //Character charA = factors.get(0).charAt(factors.get(0).length() - 1);
            //Character charB = factors.get(1).charAt(0);
            Character charA = null, charB = null;
            try {
                Duval.FactorVals vals = duval.factorVals.get(0);
                charA = text.charAt(vals.i - 1);
                charB = text.charAt(vals.j - vals.i);
            } catch(Exception e) {
                System.err.println(text);
                System.err.println(duval.factorVals.get(0).i);
                System.err.println(duval.factorVals.get(0).j);
                System.err.println(duval.factorVals.get(0).k);
                System.err.println(factors);
                System.err.println(order.toString());
                throw e;
            }

            int pos0 = order.indexOf(charB);
            Character c = order.remove(pos0);
            int pos1 = order.indexOf(charA);
            if (pos1 == order.size()) {
                order.add(c);
            } else {
                //System.err.println(order.size() + ":" + pos1);
                int max = order.size() - 1 - pos1;
                int addVal = 0;
                if (max > 0) {
                    addVal = random.nextInt(max);
                }
                order.add(pos1 + 1 + addVal, c);
            }
        }

        return order;
    }
}
