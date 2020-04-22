import java.util.ArrayList;

public class MultipleInsertionMutation extends MultipleMutation {
    public MultipleInsertionMutation(MultipleMutation nextMutation, double nextMutationChance) {
        super(nextMutation, nextMutationChance);
    }

    @Override
    protected ArrayList<Character> mutateBody(ArrayList<Character> order) {
        return new InsertionMutation().mutate(order);
    }
}
