import java.util.ArrayList;

public class MultipleScrambleMutation extends MultipleMutation {
    public MultipleScrambleMutation(MultipleMutation nextMutation, double nextMutationChance) {
        super(nextMutation, nextMutationChance);
    }

    @Override
    protected ArrayList<Character> mutateBody(ArrayList<Character> order) {
        return new ScrambleMutation().mutate(order);
    }
}
