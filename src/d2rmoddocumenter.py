#!env python

import csv,sys
import urllib.parse
import os



class d2rmoddocumenter:

    properties = {}
    sets = {}
    skills = {}
    item_types = {}
    misc = {}
    weapon_objects = {}
    armor_objects = {}
    unique_item_objects = {}
    runeword_item_objects = {}
    base_type_objects = {}
    set_item_objects = {}
    set_objects = {}
    gem_objects = {}
    all_item_objects = {}
    item_objects_by_type = {}
    item_types = {}
    _instance = None
 

    def __new__(cls, *args, **kwargs):
        """ creates a singleton object, if it is not created, or else returns the previous singleton object"""
        if not cls._instance:
            cls._instance = super(d2rmoddocumenter, cls).__new__(cls)
        return cls._instance

    def __init__(self, excel_path):
        if not excel_path:
            raise ValueError("excel_path must be provided when creating d2rmoddocumenter")
        self.excel_path = excel_path

    @classmethod
    def get_instance(cls):
        """Get the singleton instance"""
        if not cls._instance:
            raise RuntimeError("d2rmoddocumenter must be initialized with excel_path first")
        return cls._instance

    def init(self):
        print(f"Using excel_path: {self.excel_path}")
        self.read_item_types()
        self.read_properties()
        self.read_sets()
        self.read_skills()
        self.read_misc()
        self.make_gem_objects()
        self.make_weapon_objects()
        self.make_armor_objects()
        self.make_unique_item_objects()
        self.make_set_item_objects()
        self.make_set_objects()
        self.make_runeword_item_objects()

    def get_set_objects(self):
        return self.set_objects

    def get_skills(self):
        return self.skills

    def get_weapon_objects(self):
        return self.weapon_objects

    def get_armor_objects(self):
        return self.armor_objects

    def make_unique_item_objects(self):
        with open(os.path.join(self.excel_path, "uniqueitems.txt")) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for row in reader:
                if row["enabled"] != "1":
                    continue
                #print(row)
                base_type_code = row['code']
                if base_type_code == "vip": # viper amulet
                    continue
                base_type = row['*ItemName']
                name = row['index']
                item = Item(name=name, base_type=base_type)
                item.add_category("Unique")
                item.add_base_stat("Item Level", row['lvl'])
                item.add_base_stat("Level Required", row['lvl req'])
                item.add_base_stat(name="Rarity", value=row['rarity'], hidden=True)
                item.add_base_stat("base_type_code", base_type_code, hidden=True)
                ##################
                # Item Properties
                for propnum in range(1,13):
                    prop = row[f"prop{propnum}"]
                    par = row[f"par{propnum}"]
                    min = row[f"min{propnum}"]
                    max = row[f"max{propnum}"]
                    if prop:
                        #print(f"type='item', code={prop}, par={par}, min={min}, max={max}")
                        item.add_property(type="item", code=prop, par=par, min=min, max=max)
                ####################
                # Fill in stats from base type
                #print(f"basetype {base_type}")
                if base_type_code not in ["amu", "rin", "cm1", "cm2", "cm3", "jew", "mfc", "mfe", "mff"]:
                    base_type_object = self.get_base_type_object(base_type_code)            
                    #print(item.get_text())
                    #print(base_type_object.get_text())
                    try:
                        req_str = base_type_object.get_stat("Required Strength")
                    except Exception as e:
                        print(f"DEBUG: Failed to get Required Strength for {base_type_code}: {str(e)}")
                        req_str = None

                    try:
                        req_dex = base_type_object.get_stat("Required Dexterity")
                    except Exception as e:
                        print(f"DEBUG: Failed to get Required Dexterity for {base_type_code}: {str(e)}")
                        req_dex = None

                    if req_str and int(req_str) > 0:
                        item.add_base_stat("Required Strength", req_str)
                    if req_dex and int(req_dex) > 0:
                        item.add_base_stat("Required Dexterity", req_dex)
                #################
                # Save the item
                self.unique_item_objects[name] = item
                self.all_item_objects[name] = item
                if base_type not in self.item_objects_by_type:
                    self.item_objects_by_type[base_type] = {}
                self.item_objects_by_type[base_type][name] = item

    def make_runeword_item_objects(self):
        with open(os.path.join(self.excel_path, "runes.txt")) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for row in reader:
                if row["complete"] != "1":
                    continue
                #print(row)

                name = row['*Rune Name']
                item = Item(name=name, base_type="runeword")
                item.add_category("Runeword")

                ##################
                # Runeword Properties
                for propnum in range(1,8):
                    prop = row[f"T1Code{propnum}"]
                    par = row[f"T1Param{propnum}"]
                    min = row[f"T1Min{propnum}"]
                    max = row[f"T1Max{propnum}"]
                    if prop:
                        item.add_property(type="item", code=prop, par=par, min=min, max=max)
                ###################
                # Allowed types
                for typenum in range(1,6):
                    runeword_type = row[f"itype{typenum}"]
                    if runeword_type:
                        item.add_runeword_type(runeword_type)
                
                ###################
                # Required Runes
                for runenum in range(1,6):
                    rune_code = row[f"Rune{runenum}"]
                    if rune_code:
                        item.add_rune(rune_code)
                #################
                # Save the item
                self.runeword_item_objects[name] = item

    def make_gem_objects(self):
        print(f"DEBUG: Starting make_gem_objects")
        with open(os.path.join(self.excel_path, "gems.txt")) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for row in reader:
                print(f"DEBUG: Processing gem row: {row['name']}")
                #print(row)

                name = row['name']
                code = row['code']
                if "Chipped" in name or "Flawed" in name:
                    continue

                if "Rune" in name:
                    base_type = "rune"
                    category = "Rune"
                else:
                    base_type = "gem"
                    category = "Gem"

                item = Item(name=name, base_type=base_type)
                item.add_category(category)

                ##################
                # Weapon Properties
                for propnum in range(1,4):
                    prop = row[f"weaponMod{propnum}Code"]
                    par = row[f"weaponMod{propnum}Param"]
                    min = row[f"weaponMod{propnum}Min"]
                    max = row[f"weaponMod{propnum}Max"]
                    if prop:
                        print(f"DEBUG: Adding weapon property to gem {name}: {prop}")
                        item.add_property(type="gem_weapon", code=prop, par=par, min=min, max=max)
                for propnum in range(1,4):
                    prop = row[f"helmMod{propnum}Code"]
                    par = row[f"helmMod{propnum}Param"]
                    min = row[f"helmMod{propnum}Min"]
                    max = row[f"helmMod{propnum}Max"]
                    if prop:
                        item.add_property(type="gem_helm", code=prop, par=par, min=min, max=max)
                for propnum in range(1,4):
                    prop = row[f"shieldMod{propnum}Code"]
                    par = row[f"shieldMod{propnum}Param"]
                    min = row[f"shieldMod{propnum}Min"]
                    max = row[f"shieldMod{propnum}Max"]
                    if prop:
                        item.add_property(type="gem_shield", code=prop, par=par, min=min, max=max)

                
                #################
                # Save the item
                self.gem_objects[code] = item


    def make_set_objects(self):
        with open(os.path.join(self.excel_path, "sets.txt")) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for row in reader:
                #print(row)
                name = row["name"]
                if not name:
                    continue
                name = name.replace("McAuley's", "Sander's")
                set = Item(name=name, base_type="set")
                set.add_category("Set")

                ##########################
                # Partial Set Bonuses
                for setpropnum in range(2,6):
                    for setpropletter in ["a","b"]:
                        prop = row[f"PCode{setpropnum}{setpropletter}"]
                        par = row[f"PParam{setpropnum}{setpropletter}"]
                        min = row[f"PMin{setpropnum}{setpropletter}"]
                        max = row[f"PMax{setpropnum}{setpropletter}"]
                        if prop:
                            #print(f"type='item', code={prop}, par={par}, min={min}, max={max}")
                            type = f"set{setpropnum}"
                            set.add_property(type=type, code=prop, par=par, min=min, max=max)
                #######################
                # Full Set Bonuses
                for fullnum in range(1,9):
                    prop = row[f"FCode{fullnum}"]
                    par = row[f"FParam{fullnum}"]
                    min = row[f"FMin{fullnum}"]
                    max = row[f"FMax{fullnum}"]
                    if prop:
                        #print(f"type='item', code={prop}, par={par}, min={min}, max={max}")
                        type = f"setfull"
                        set.add_property(type=type, code=prop, par=par, min=min, max=max)
                #######################
                # Set Items
                for set_item_name in self.set_item_objects.keys():
                    item = self.set_item_objects[set_item_name]
                    item_set = item.get_set()
                    if item.get_set() == name:
                        # set up the relationship between set and item in both directions
                        set.add_set_item(item)
                        item.add_set_object(set)

                self.set_objects[name] = set





    def make_set_item_objects(self):
        with open(os.path.join(self.excel_path, "setitems.txt")) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for row in reader:
                if row["*ID"]:

                    #print(row)
                    base_type_code = row['item'].strip()
                    base_type = row['*ItemName'].strip()
                    # Correct for Errors
                    if base_type == "Ornate Plate":
                        base_type = "Ornate Armor"
                    if base_type == "Sabre":
                        base_type = "Saber"
                    if base_type == "Colossus Sword":
                        base_type = "Colossal Sword"
                    name = row['index'].strip()
                    if not name:
                        continue
                    name = name.replace("McAuley's", "Sander's")
                    item = Item(name=name, base_type=base_type)
                    item.add_category("SetItem")
                    item.add_base_stat("Item Level", row['lvl'])
                    item.add_base_stat("Level Required", row['lvl req'])
                    parent_set = row['set']
                    parent_set = parent_set.replace("McAuley's", "Sander's")
                    item.add_base_stat("Set", parent_set)
                    item.add_base_stat("base_type_code", base_type_code, hidden=True)
                    item.add_base_stat(name="Rarity", value=row['rarity'], hidden=True)
                    #####################
                    # Item Properties
                    for propnum in range(1,10):
                        prop = row[f"prop{propnum}"]
                        par = row[f"par{propnum}"]
                        min = row[f"min{propnum}"]
                        max = row[f"max{propnum}"]
                        if prop:
                            #print(f"type='item', code={prop}, par={par}, min={min}, max={max}")
                            item.add_property(type="item", code=prop, par=par, min=min, max=max)
                    ####################
                    # Item Set Bonuses
                    for setpropnum in range(1,6):
                        for setpropletter in ["a","b"]:
                            prop = row[f"aprop{setpropnum}{setpropletter}"]
                            par = row[f"apar{setpropnum}{setpropletter}"]
                            min = row[f"amin{setpropnum}{setpropletter}"]
                            max = row[f"amax{setpropnum}{setpropletter}"]
                            if prop:
                                #print(f"type='item', code={prop}, par={par}, min={min}, max={max}")
                                set_items_required = setpropnum + 1
                                type = f"set{set_items_required}"
                                item.add_property(type=type, code=prop, par=par, min=min, max=max)
                    ####################
                    # Fill in stats from base type
                    #print(f"basetype {base_type}")
                    if base_type_code not in ["amu", "rin"]:
                        base_type_object = self.get_base_type_object(base_type_code)            
                        req_str = base_type_object.get_stat("Required Strength")
                        req_dex = base_type_object.get_stat("Required Dexterity")
                        if req_str:
                            item.add_base_stat("Required Strength", req_str)
                        if req_dex:
                            item.add_base_stat("Required Dexterity", req_dex)
               

                    self.set_item_objects[name] = item
                    self.all_item_objects[name] = item
                    if base_type not in self.item_objects_by_type:
                        self.item_objects_by_type[base_type] = {}
                    self.item_objects_by_type[base_type][name] = item





    def make_weapon_objects(self):
        print(f"Making weapon objects from {os.path.join(self.excel_path, 'weapons.txt')}")
        with open(os.path.join(self.excel_path, "weapons.txt")) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for row in reader:
                #print(row)
                #print("\n\n")
                #for k in row.keys():
                    #print(f"{k}: {row[k]}")
                name = row['name'].strip()
                type = row['type'].strip()
                code = row['code'].strip()
                if not type:
                    continue
                base_type = BaseType(name=name, code=code)
                base_type.add_category(type, self.item_types[type]['ItemType'], primary=True)
                type2 = self.item_types[type]["Equiv1"].strip()
                if type2:
                    base_type.add_category(type2, self.item_types[type2]['ItemType'], primary=False)
                type3 = self.item_types[type]["Equiv2"].strip()
                if type3:
                    base_type.add_category(type3, self.item_types[type3]['ItemType'], primary=False)
                base_type.add_stat(name="code", value=row["code"], hidden=True)
                base_type.add_stat(name="normalcode", value=row["normcode"], hidden=True)
                base_type.add_stat(name="exceptionalcode", value=row["ubercode"], hidden=True)
                base_type.add_stat(name="elitecode", value=row["ultracode"], hidden=True)
                if code == row["normcode"]:
                    difficultylevel = "Normal"
                elif code == row["ubercode"]:
                    difficultylevel = "Exceptional"
                elif code == row["ultracode"]:
                    difficultylevel = "Elite"
                else:
                    # Special items such as khalims will dont follow these rules
                    pass
                base_type.add_stat(name="Difficulty Level", value=difficultylevel)
                base_type.add_damage(type="1 Handed", min=row["mindam"], max=row["maxdam"])
                base_type.add_damage(type="2 Handed", min=row["2handmindam"], max=row["2handmaxdam"])
                base_type.add_damage(type="Throw", min=row["minmisdam"], max=row["maxmisdam"])
                base_type.add_stat(name="Rarity", value=row["rarity"], hidden=True)
                base_type.add_stat(name="Required Strength", value=row["reqstr"])
                base_type.add_stat(name="Required Dexterity", value=row["reqdex"])
                base_type.add_stat(name="Required Dexterity", value=row["reqdex"])
                base_type.add_stat(name="Max Sockets", value=row["gemsockets"])
                base_type.add_stat(name="Socket Type", value=self.get_socket_type_description(row["gemapplytype"]))
                base_type.add_stat(name="Required Level", value=row["levelreq"])
                base_type.add_stat(name="Attack Speed", value=row["speed"])
                base_type.add_stat(name="Quality Level", value=row["level"])
                base_type.add_stat(name="Range", value=row["rangeadder"])
                self.weapon_objects[code] = base_type
                self.base_type_objects[code] = base_type


    def make_armor_objects(self):
        with open(os.path.join(self.excel_path, "armor.txt")) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for row in reader:
                #print(row)
                #print("\n\n")
                #for k in row.keys():
                    #print(f"{k}: {row[k]}")
                name = row['name'].strip()
                code = row['code'].strip()
                type1 = row['type'].strip()
                if not type1:
                    continue
                if not code:
                    continue
                #for k in self.item_types.keys():
                    #print(k)
                base_type = BaseType(name=name, code=code)
                base_type.add_category(type1, self.item_types[type1]['ItemType'], primary=True)
                type2 = self.item_types[type1]["Equiv1"].strip()
                if type2:
                    base_type.add_category(type2, self.item_types[type2]['ItemType'], primary=False)
                type3 = self.item_types[type1]["Equiv2"].strip()
                if type3:
                    base_type.add_category(type3, self.item_types[type3]['ItemType'], primary=False)

                base_type.add_stat(name="code", value=row["code"], hidden=True)
                base_type.add_stat(name="normalcode", value=row["normcode"], hidden=True)
                base_type.add_stat(name="exceptionalcode", value=row["ubercode"], hidden=True)
                base_type.add_stat(name="elitecode", value=row["ultracode"], hidden=True)
                if code == row["normcode"]:
                    difficultylevel = "Normal"
                elif code == row["ubercode"]:
                    difficultylevel = "Exceptional"
                elif code == row["ultracode"]:
                    difficultylevel = "Elite"
                else:
                    raise Exception(f"Could not figure out item {name} quality level")
                base_type.add_stat(name="Difficulty Level", value=difficultylevel)
                base_type.add_stat(name="Rarity", value=row["rarity"], hidden=True)
                if row["reqstr"] and int(row["reqstr"]) > 0:
                    base_type.add_stat(name="Required Strength", value=row["reqstr"])
                if row["reqdex"] and int(row["reqdex"]) > 0:
                    base_type.add_stat(name="Required Dexterity", value=row["reqdex"])
                base_type.add_stat(name="Max Sockets", value=row["gemsockets"])
                base_type.add_stat(name="Socket Type", value=self.get_socket_type_description(row["gemapplytype"]))
                base_type.add_stat(name="Required Level", value=row["levelreq"])
                base_type.add_stat(name="Quality Level", value=row["level"])
                if type1 == "boot":
                    base_type.add_damage(type="Kick", min=row['mindam'], max=row['maxdam'])
                if type1 == "shie":
                    base_type.add_damage(type="Smite", min=row['mindam'], max=row['maxdam'])
                base_type.add_ac(min=row["minac"], max=row["maxac"])
 

                self.armor_objects[code] = base_type
                self.base_type_objects[code] = base_type




    def get_gem(self, code):
        if code in self.gem_objects:
            return self.gem_objects[code]
        else:
            return None

    def get_gem_by_name(self, name):
        for code in self.gem_objects.keys():
            if self.gem_objects[code].get_name() == name:
                return self.gem_objects[code]
        return None

    def get_gem_objects(self):
        return self.gem_objects
 
    def get_unique_item_objects(self):
        return self.unique_item_objects

    def get_runeword_item_objects(self):
        return self.runeword_item_objects

    def get_all_item_objects(self):
        return self.all_item_objects

    def get_set_item_objects(self):
        return self.set_item_objects

    def get_properties(self):
        return self.properties

    def read_properties(self):
        with open(os.path.join(self.excel_path, "properties.txt")) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for row in reader:
                self.properties[row["code"]] = row

    def get_property(self, code):
        if code in self.properties:
            return self.properties[code]
        else:
            return None

    def get_base_type_object(self, code):
        if code in self.base_type_objects:
            return self.base_type_objects[code]
        else:
            return None

    def get_socket_type_description(self, socket_type):
        if int(socket_type) == 0:
            return "Weapon"
        if int(socket_type) == 1:
            return "Armor/Helmet"
        elif int(socket_type) == 2:
            return "Shield"
        else:
            return "Unknown"
     


    def read_skills(self):
        with open(os.path.join(self.excel_path, "skills.txt")) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for row in reader:
                self.skills[row["*Id"]] = row 

    def get_skill(self, id):
        return self.skills[id]

    def read_sets(self):
        with open(os.path.join(self.excel_path, "sets.txt")) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for row in reader:
                self.sets[row["index"]] = row 

    def read_item_types(self):
        with open(os.path.join(self.excel_path, "itemtypes.txt")) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for row in reader:
                if not row["Code"]:
                    continue
                #print("\n")
                #print(row)
                self.item_types[row["Code"]] = row 

    def read_misc(self):
        with open(os.path.join(self.excel_path, "misc.txt")) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for row in reader:
                self.misc[row["name"]] = row 


              
#############################################################
# The item class provides a bit of a standardized version of 
# special items - ie. set items, unique items, runewords
class Item:

    name = None
    base_type = None
    category = None
    level_required = None
    base_stats = {}
    properties = {}
    set_items = []
    runes = []
    runeword_types = []
    set_object = None

    def __init__(self, name="", base_type=""):
        if not name or not base_type:
            raise Exception(f"Tried to create an item ({name}) without a name or base type")
        self.name = name
        self.base_type = base_type
        self.properties = {}
        self.base_stats = {}
        self.set_items = []
        self.runes = []
        self.runeword_types = []
        self.level_required = None
        self.category = "Unknown_Category"

    def add_base_stat(self, name="", value="", hidden=False):
        if not name or not value:
            raise Exception("Tried to add a base stat without a name or value")
        self.base_stats[name] = {"name": name, "value": value, "hidden": hidden}

    def add_runeword_type(self, type):
        self.runeword_types.append(type)

    def add_rune(self, rune_code):
        documenter = d2rmoddocumenter.get_instance()
        rune = documenter.get_gem(rune_code)
        self.runes.append(rune_code)

        rune_properties = rune.get_properties()

        ####################
        # properties for shields
        shield_types = ["shld", "pala"]
        l = [t for t in self.runeword_types if t in shield_types ]
        if len(l) > 0:
            if "gem_shield" not in self.properties:
                self.properties["gem_shield"] = []
            self.properties["gem_shield"].extend(rune_properties["gem_shield"])

        #####################
        # Properties for helms and armor
        helm_and_armor_types = ["tors", "helm"]
        l = [t for t in self.runeword_types if t in helm_and_armor_types ]
        if len(l) > 0:
            if "gem_helm" not in self.properties:
                self.properties["gem_helm"] = []
            self.properties["gem_helm"].extend(rune_properties["gem_helm"])

        #####################
        # Properties for weapons
        weapon_types = [
            "mele", "club", "hamm", "mace", "swor", "miss", "weap", "h2h", "axe", "pole",
            "spear", "staf", "scep", "knif", "wand" ]
        l = [t for t in self.runeword_types if t in weapon_types ]
        if len(l) > 0:
            if "gem_weapon" not in self.properties:
                self.properties["gem_weapon"] = []
            self.properties["gem_weapon"].extend(rune_properties["gem_weapon"])





    def add_set_item(self, item):
        if self.base_type != "set":
            raise Exception("Tried to add a set item to something that is not a set")
        self.set_items.append(item)

    def add_set_object(self, set):
        self.set_object=set

    def add_category(self, category):
        self.category = category

    def get_category(self):
        return self.category

    def add_property(self, type="", code="", par="", min="", max=""):
        if not type or not code:
            raise Exception("Tried to add a property stat without a type or code(name)")
        if type not in self.properties:
            self.properties[type] = []
        code = code.lower()

        # Use the singleton instance
        documenter = d2rmoddocumenter.get_instance()
        base_property = documenter.get_property(code)
        if not base_property:
            return

        property = {}
        property["name"] = code
        property["par"] = par
        property["min"] = min
        property["max"] = max
        property["tooltip"] = self.get_property_tooltip(property)
        self.properties[type].append(property)

    def get_properties_by_type(self, type):
        if type in self.properties:
            return self.properties[type]
        else:
            return []

    def get_properties(self):
        return self.properties

    def get_set(self):
        if "Set" in self.base_stats:
            return self.base_stats["Set"]["value"]
        else:
            return None

    def get_name(self):
        return self.name

    def get_rune_shortname(self):
        return self.name.replace(" Rune", "")

    def get_nice_name(self):
        nn = self.name.replace("'", "")
        nn = nn.replace(" ", "_")
        nn = urllib.parse.quote(nn)
        return nn

    def get_path(self):
        return f"Items/{self.category}"

    def get_base_filename(self):
        nn = self.get_nice_name()
        link = f"{nn}"
        return link

    def get_link(self):
        if self.set_object is not None:
            link = f"{self.set_object.get_link()}#{self.get_nice_name()}"
        elif self.base_type == "gem":
            link = f"Gems#{self.get_nice_name()}"
        else:
            link = f"{self.get_path()}/{self.get_base_filename()}"
        return link


    def get_text(self, show_hidden=False, allow_redirect=True, child=False):

        documenter = d2rmoddocumenter.get_instance()

        if self.base_type == "set":
            return self.get_text_set(show_hidden=show_hidden, allow_redirect=allow_redirect, child=child)

        item_text = ""

        # if accessed directly, set items should redirect onto the set page
        if self.set_object is not None and allow_redirect:
            return f"#REDIRECT {self.get_link()}\n\n"

        item_text += "{| class=\"wikitable\"\n"

        if self.base_type in ["gem", "rune"]:
            item_text += "|-\n| {{" + self.get_nice_name() + "}}\n"

        item_text += f'|-\n! colspan="2" | [[{self.get_link()}|{self.name}]]\n'
        if self.base_type not in ["set", "runeword"]:
            item_text += f"|-\n| Base Type || {self.base_type}\n"
        if len(self.runes) > 0:
            item_text += f"|-\n| Runes || "
            for rune_code in self.runes:
                rune = documenter.get_gem(rune_code) 
                item_text += f" {rune.get_rune_shortname()}"
            item_text += f"\n"

        for base_stat_name in self.base_stats.keys():
            if not self.base_stats[base_stat_name]["hidden"]:
                if base_stat_name == "Set":
                    item_text += f"|-\n| Set || [[{self.set_object.get_link()}|{self.set_object.get_name()}]]\n"
                else:
                    item_text += f"|-\n| {base_stat_name} || {self.base_stats[base_stat_name]['value']}\n"

            
        item_text += '|-\n| colspan="2" style="text-align:center; font-weight:bold;" | Properties\n'
        for property_type in self.properties.keys():
            # item_text += "|-\n"
            if "set" in property_type:
                items_required = property_type[3:]
                item_text += f'|-\n| colspan="2" style="text-align:center; font-weight:bold" | Set Bonus for {items_required} Items\n'
            # I dont think we should be dealing with gems here, its too confusing
            if "gem_" in property_type:
                gem_property_type = property_type[4:]
                if gem_property_type == "helm":
                    gem_property_type_desc = "Helmet or Armor"
                elif gem_property_type == "weapon":
                    gem_property_type_desc = "Weapon"
                elif gem_property_type == "shield":
                    gem_property_type_desc = "Shield"
                else:
                    gem_property_type_desc = gem_property_type
                item_text += f"| When used in a {gem_property_type_desc}\n"
            for property in self.properties[property_type]:
                item_text += f"|-\n| colspan=\"2\" | {property['tooltip']}\n\n"
        item_text += "|}\n"
        item_text += "\n\n"

        return item_text


    def get_text_gem(self, write_table=False, color=None):

        documenter = d2rmoddocumenter.get_instance()

        colortext = ""
        if color:
            colortext = f" style=\"color:{color};\" | "

        item_text = ""

        if write_table:
            item_text += "{| class=\"wikitable\"\n"
            item_text += "|-\n! Name !! Helmet or Armor !! Weapon !! Sheild\n"

        item_text += "|-\n"
        item_text += f"| {colortext}{self.get_name()}"

            
        property_types = ["gem_helm", "gem_weapon", "gem_shield"]
        for ptype in property_types:
            item_text += " ||"
            for property in self.properties[ptype]:
                item_text += f" {property['tooltip']}<br>"
        item_text += "\n"

        if write_table:
            item_text += "|}\n"

        return item_text


    def get_text_set(self, show_hidden=False, allow_redirect=True, child=False):

        documenter = d2rmoddocumenter.get_instance()
        item_text = ""

        if len(self.set_items) > 0:
            for set_item in self.set_items:
                item_text += "\n\n"
                item_text += set_item.get_text(show_hidden, allow_redirect=False)

        item_text += "{| class=\"wikitable\"\n"

        item_text += f'|-\n! colspan="2" | Set Bonuses\n'

        for property_type in self.properties.keys():
            # item_text += "|-\n"
            if "set" in property_type:
                items_required = property_type[3:]
                item_text += f'|-\n| colspan="2" style="text-align:center; font-weight:bold" | Set Bonus for {items_required} Items\n'
            for property in self.properties[property_type]:
                item_text += f"|-\n| colspan=\"2\" | {property['tooltip']}\n"
        item_text += "|}\n"
        item_text += "\n\n"


        return item_text

    
    def get_property_tooltip(self, property=property):
        # name is actually a short code to look up in properties.txt
        name = property["name"]
        par = property["par"]
        min = property["min"]
        max = property["max"]
        documenter = d2rmoddocumenter.get_instance()
        base_property = documenter.get_property(name)
 
        if not base_property:
            # print(f"Unknown property {name}")
            return ""

        # Ironstone has *enr but it isnt in properties.txt and doesnt do anything - skip it
        if name == "*enr":
            return ""
    
        # fix wrong case for duskdeep
        if name == "Dex":
            name = "dex"
    
        tooltip = base_property['*Tooltip']

        #print(f"{tooltip} par {par} min {min} max {max}")
    
        if name == "res-all-max":
            tooltip = "+#% Maximum to all Resistances"

        if "randclassskill" in name:
            pskills = base_property["val1"]
            tooltip = f"+{pskills} to Random Class Skill Levels"
    
        if name == "dmg-pois":
            #print(f"{tooltip} par {par} min {min} max {max}")
            # I think this defaults to 6 seconds ( in # of frames )
            # Black tounge is par 150 min 192 max 192 and does 113 over 6 sec
            # Hellplague is par min 150 max 150 and does 88 over 6 seconds
            # 113 = 192 * x * 150
            if not par:
                par = "150"
            seconds = int(par) / 25
            mindam = int(int(min) / 256 * int(par))
            maxdam = int(int(max) / 256 * int(par))
            if mindam == maxdam:
                tooltip = f"+{mindam} Poison Damage over {seconds} Seconds"
            else:
                tooltip = f"+{mindam}-{maxdam} Poison Damage over {seconds} Seconds"

        if name == "pois-len":
            if par and par != "0":
                length = int(int(par)/25)
            else:
                if max == min:
                    length = int(int(max)/25)
                else:
                    length = f"{int(int(min)/25)}-{int(int(max)/25)}"
            tooltip = f"Poison Length {length} seconds"

        if name == "cold-len":
            if par and par != "0":
                length = int(int(par)/25)
            else:
                if max == min:
                    length = int(int(max)/25)
                else:
                    length = f"{int(int(min)/25)}-{int(int(max)/25)}"
            tooltip = f"Cold Length {length} seconds"
    
        if name == "pierce":
            tooltip = "+#% Piercing Attack"

        if name == "splash":
            #tooltip = f"Spash Damage {min}"
            tooltip = "Applies Splash Damage"
        
        raw_tooltip = tooltip
    
        if "[Skill]" in tooltip:
            if par.isnumeric():
                documenter = d2rmoddocumenter.get_instance()
                skill = documenter.get_skill(par)["skill"]
            else: 
                skill = par

            if skill == "Quickness":
                skill = "Burst of Speed"

            tooltip = tooltip.replace("[Skill]", skill)
    
        if "when struck" in tooltip:
            tooltip = tooltip.replace("#%", f"{min}%")
            tooltip = tooltip.replace("#", max)
    
        if "when you Die" in tooltip:
            tooltip = tooltip.replace("#%", f"{min}%")
            tooltip = tooltip.replace("#", max)
    
        if min > max:
            temp = min
            min = max
            max = temp
    
        if "Better Chance of Getting Magic Items (Based on Character Level)" in tooltip:
            #print(f"{tooltip} par {par} min {min} max {max}")
            if par:
                percent = int(par) / 8
                tooltip = tooltip.replace("#%", f"( {percent}% per clvl )")
            elif min == max:
                percent = int(max)/8
            else:
                percent = f"{int(min)/8}-{int(max)/8}"
            tooltip = tooltip.replace("#%", f"( {percent}% per clvl )")
    
        tooltip = tooltip.replace("#-#", f"#")

        if max:
            if max == min: 
                tooltip = tooltip.replace("#", f"{max}")
            else:
                tooltip = tooltip.replace("#", f"{min}-{max}")
    
        if name == "skill-rand":
            tooltip = f"+{par} to a Random Skill"

        tooltip = tooltip.replace("+-", f"-")
        tooltip = tooltip.replace("--", f"-")

        return tooltip



####################################
# BaseItem class provides a standardized version of normal/base items ( ie. whites )
class BaseType:

    name = None
    code = None
    ac = None
    stats = {}
    damage = {}
    categories = []

    def __init__(self, name="", code=""):
        if not name or not type:
            raise Exception("Tried to create an item without a name or base type")
        self.stats = {}
        self.damage = {}
        self.name = name
        self.code = code
        self.ac = None
        self.categories = []

    def add_stat(self, name="", value="", hidden=False):
        if not name:
            raise Exception("Tried to add a base stat without a name")
        if value:
            self.stats[name] = {"name": name, "value": value, "hidden": hidden}

    def add_damage(self, type="", min=0, max=0):
        if not type:
            raise Exception("Tried to add damage without a type")
        if not min or not max:
            return
        intmin = int(min)
        intmax = int(max)
        if intmin > 0 and intmax > 0:
            self.damage[type] = {"type": type, "min": intmin, "max": intmax}

    def add_category(self, code, desc, primary=False):
        hidden = False
        desc = desc.rstrip("s")
        if code == "helm":
            desc = "Helmet"
        if code == "shld":
            # Any Shield
            hidden = True 
        if code == "armo":
            # This is any armor
            hidden = True
        if code == "merc":
            # we would need to recurse through categories in order for this to be useful
            #self.add_stat(name="Mercenary Equipable", value="True")
            hidden = True
        self.categories.append( { "code": code, "desc": desc, "hidden": hidden, "primary": primary } )
    

    def add_ac(self, min=0, max=0):
        if not min or not max:
            return
        intmin = int(min)
        intmax = int(max)
        if intmin > 0 and intmax > 0:
            self.ac = {"min": intmin, "max": intmax}

    def get_stat(self, name):
        if not name:
            raise Exception("Tried to get a stat without a name")
        if name == "type":
            return self.type
        if name in self.stats:
            return self.stats[name]["value"]
        return None

    def get_text(self, show_hidden=False, html=False, indent=0):
        if html:
            newline = "<br>\n"
        else:
            newline = "\n"
        indenttext = indent * "    "
        item_text = ""
        item_text += f"{indenttext}=== {self.name} ==={newline}"
        if show_hidden:
            item_text += f"{indenttext}Code: {self.code}{newline}"
        for cat in self.categories:
            if show_hidden or not cat["hidden"]:
                if show_hidden:
                    catcode = f" ({cat['code']})"
                else:
                    catcode = ""
                item_text += f"{indenttext}{cat['desc']}{catcode}{newline}"
        for damtype in self.damage.keys():
            if len(self.damage) == 1 and damtype not in ["Smite", "Kick"]:
                item_text += f"{indenttext}{self.damage[damtype]['min']}-{self.damage[damtype]['max']} Damage{newline}"
            else:
                item_text += f"{indenttext}{self.damage[damtype]['min']}-{self.damage[damtype]['max']} {damtype} Damage{newline}"
        if self.ac:
            if self.ac['min'] == self.ac['max']:
                item_text += f"{indenttext}{self.ac['min']} Defense{newline}"
            else:
                item_text += f"{indenttext}{self.ac['min']}-{self.ac['max']} Defense{newline}"
        for stat_name in self.stats.keys():
            if show_hidden or not self.stats[stat_name]["hidden"]:
                item_text += f"{indenttext}{stat_name}: {self.stats[stat_name]['value']}{newline}"
        return item_text
