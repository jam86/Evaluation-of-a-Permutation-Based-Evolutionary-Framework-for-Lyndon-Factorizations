import java.util.ArrayList;
import java.util.Random;

public abstract class MultipleMutation implements Mutation {
    private MultipleMutation nextMutation;
    private double nextMutationChance;
    private Random random = new Random();

    public MultipleMutation(MultipleMutation nextMutation, double nextMutationChance) {
        this.nextMutation = nextMutation;
        this.nextMutationChance = nextMutationChance;
    }

    public ArrayList<Character> mutate(ArrayList<Character> order) {
        ArrayList<Character> newOrder = mutateBody(order);

        if (nextMutation != null && random.nextDouble() % 100 <= nextMutationChance) {
            return nextMutation.mutate(newOrder);
        }

        return newOrder;
    }

    protected abstract ArrayList<Character> mutateBody(ArrayList<Character> order);

    @Override
    public String toString() {
        return this.getClass().getName() + (nextMutation != null? " (" + nextMutationChance + "%) -> " + nextMutation.toString() : "");
    }
}
