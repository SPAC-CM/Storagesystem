SQLManager manager = SQLManager.Instance;

manager.set_connection(args[0],args[1],args[2]);
manager.insert();
