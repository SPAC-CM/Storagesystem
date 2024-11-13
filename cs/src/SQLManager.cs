using MySql.Data.MySqlClient;
using DatabaseWrapper.Core;
using ExpressionTree;
using Watson.ORM.Core;
using Watson.ORM.Mysql;

//The table coulumn takes just a name
[Table("Catagories")]
public class Catagory
{

	//A column takes first name, then if it is the primary key, the datatype and if it is nullalble
	[Column("CatagoryID", true, DataTypes.Int, false)]
	public int Id { get; set; }
	
	//For strings, you also add the mac lengt
	[Column("CatagoryName", false, DataTypes.Nvarchar, 15, false)]
	public string CatagoryName { get; set; }

	// Parameter-less constructor is required
	public Catagory()
  	{
  	}
}

public sealed class SQLManager
{
	private static readonly SQLManager instance = new SQLManager();
	
	private static WatsonORM? orm;

	private SQLManager()
	{
	}
	
	static SQLManager()
	{
	}

	public static SQLManager Instance { get {return instance;}}

	public void set_connection(string user, string password, string database)
	{
		DatabaseSettings settings = new DatabaseSettings(DbTypeEnum.Mysql,"localhost",3306,user,password,database);
		orm = new WatsonORM(settings);
		orm.InitializeDatabase();

	}

	public void insert()
	{
		if(orm is not null)
		{
			orm.InitializeTables(new List<Type>{typeof(Catagory)});
			Catagory catagory = new Catagory{CatagoryName = "Better Stuffs"};
			orm.Insert<Catagory>(catagory);
		}

	}
}
