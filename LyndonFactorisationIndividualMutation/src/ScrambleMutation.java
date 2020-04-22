import java.util.ArrayList;
import java.util.Collections;
import java.util.Random;

public class ScrambleMutation implements Mutation {
    private Random random = new Random();

    public ArrayList<Character> mutate(ArrayList<Character> order) {
        // do a scramble mutation
        // choose 2 positions and randomise the positions between them
        int pos0 = random.nextInt(order.size());
        int pos1 = pos0;
        while(pos1 == pos0) {
            pos1 = random.nextInt(order.size());
        }

        ArrayList<Character> tempChars = new ArrayList<>();
        for (int i = Math.min(pos0, pos1); i < Math.max(pos0, pos1); i++) {
            tempChars.add(order.get(i));
        }
        Collections.shuffle(tempChars, random);

        for (int i = 0; i < tempChars.size(); i++) {
            order.set(i + Math.min(pos0, pos1), tempChars.get(i));
        }

        return order;
    }
}
