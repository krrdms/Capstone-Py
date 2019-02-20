"""
MacLookup Library - code for pulling in OUI Table and checking MAC address against it
"""

from urllib.request import urlopen
import ssl


class MacLookUpTableItem:

    """
    Initialization function __init__
    :param mac_oui (String)
    :param short_name (Strng)
    :param long_name (String)
    """
    def __init__(self, mac_oui, short_name,long_name):
        self.mac_oui = mac_oui
        self.short_name = short_name
        self.long_name = long_name


class MacLookup:

    # Initializer
    # input validation on MAC
    #  convert MAC into ints and split to octets
    ###### - JKA

    """
    Initialization function __init__
    :param mac_address - (String) mac_address to match/search
    """
    def __init__(self, mac_address):
        hex_octets = []
        self.lookup_item_list = []

        if self.how_many_char(":-", mac_address) != 0:
            octets = mac_address.replace("-", ":").split(":")
            for octet in octets:
                hex_octets.append(hex(int("0x" + octet, 16))[2:])
            self.mac_address = hex_octets
        else:
            raise Exception('Mac address not properly formatted')

    """
    Retrieve OUI Table from wireshark website
    Only deal with 3 digit OUI for not
    Todo: - need to code for storage of 6 digit OUI and masks
    :return (Bool) True on success - else False
    """
    def retrieve_oui_table (self):
        ssl._create_default_https_context = ssl._create_unverified_context
        oui_table = "https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf"

        for line in urlopen(oui_table):
            line_split = str(line, 'utf-8').split("\t")

            if len(line_split) == 3:
                this_oui_instance = MacLookUpTableItem (line_split[0],line_split[1],line_split[2])
                self.lookup_item_list.append (this_oui_instance)
            else:
                 return False

        print("loaded items from Wireshark list: " + str (len(self.lookup_item_list)))
        return True
    # def macLookup (self):
    #    pass

    def print_oui_reference(self):
        for item in self.lookup_item_list:
            print(item.mac_oui + " " + item.short_name)

    """
    Count how many times a character appears in a string
    Utility function - Todo - move to utility library
    :param char (String)
    :param input_string (String)
    :return int (Int) - number of matches - >0 - equal at least one match - 0 - none
    """
    def how_many_char(self, char, input_string):
        return len([x for x in input_string if x in char])


ml = MacLookup ("00-50-56-c0-00-08")
ml.retrieve_oui_table()
# ml.print_oui_reference()


