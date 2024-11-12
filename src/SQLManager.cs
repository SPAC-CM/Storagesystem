public sealed class SQLManager
{
	private static readonly SQLManager instance = new SQLManager();
	
	static SQLManager()
	{
	}

	public static SQLManager Instance { get {return instance;}}

}
