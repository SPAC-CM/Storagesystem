using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace cs.src
{
    public class DefualtProduct : I_Product
    {
        public int ID { get; set; }
        public string produckName { get; set; }

        public DefualtProduct(int ID, string produckName)
        {
            this.ID = ID;
            this.produckName = produckName;
        }
    }
    
    public class Shoe : I_Product
    {
        public int ID { get; set; }
        public string produckName { get; set; } = string.Empty;

        public Shoe(int ID, string produckName)
        {
            this.ID = ID;
            this.produckName = produckName;
        }

    }
}