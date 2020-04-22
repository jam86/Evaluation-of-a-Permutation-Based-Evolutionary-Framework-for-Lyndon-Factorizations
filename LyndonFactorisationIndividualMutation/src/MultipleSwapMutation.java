import java.util.ArrayList;

public class MultipleSwapMutation extends MultipleMutation {
    public MultipleSwapMutation(MultipleMutation nextMutation, double nextMutationChance) {
        super(nextMutation, nextMutationChance);
    }

    @Override
    protected ArrayList<Character> mutateBody(ArrayList<Character> order) {
        return new SwapMutation().mutate(order);
    }
}
