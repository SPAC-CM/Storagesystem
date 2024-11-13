using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace cs.src
{
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
}