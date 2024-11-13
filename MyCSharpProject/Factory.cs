
public abstract class Factory
{
    public virtual I_Product Create(int ID, string produckName)
    {
        return new DefualtProduct(0, "");
    }
}

public class ShoeFactory : Factory
{
    public override Shoe Create(int ID, string produckName)
    {
        return new Shoe(ID, produckName);
    }
}
