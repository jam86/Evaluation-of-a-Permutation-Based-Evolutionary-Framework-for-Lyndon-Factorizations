import java.util.ArrayList;
import java.util.Collections;
import java.util.Random;

public class InsertionMutation implements Mutation {
    private Random random = new Random();

    public ArrayList<Character> mutate(ArrayList<Character> order) {
        // do an insertion mutation
        // choose 2 positions and insert the character at pos0 at pos1, shifting other characters
        int pos0 = random.nextInt(order.size());
        int pos1 = pos0;
        while(pos1 == pos0) {
            pos1 = random.nextInt(order.size());
        }

        char tempCharacter = order.remove(pos0);
        order.add(pos1, tempCharacter);

        return order;
    }
}
