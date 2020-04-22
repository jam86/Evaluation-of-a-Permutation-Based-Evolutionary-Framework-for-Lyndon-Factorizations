import java.util.ArrayList;
import java.util.Random;

public class SwapMutation implements Mutation {
    private Random random = new Random();

    public ArrayList<Character> mutate(ArrayList<Character> order) {
        // do a swap mutation
        int pos0 = random.nextInt(order.size());
        int pos1 = pos0;
        while(pos1 == pos0) {
            pos1 = random.nextInt(order.size());
        }

        char temp = order.get(pos0);
        order.set(pos0, order.get(pos1));
        order.set(pos1, temp);

        return order;
    }
}
