#!/usr/bin/python3
import logging
import sys

inputs = [
        'D2FE28', # 2021 val
        '38006F45291200', # 2 subpackets 10, 20
        'EE00D40C823060', # 3 sub packets 1,2,3
        '8A004A801A8002F478', #16           
        '620080001611562C8802118E34',
        'C0015000016115A2E0802F182340'
        'A0016C880162017C3686B18A3D4780',
        'C200B40A82', #  1+ 2 =3
        '04005AC33890', # 6*9
        '880086C3E88112', # min 7,8,9
        'CE00C43D881120', # max 7,8,9
        'D8005AC2A8F0', # 5< 15 ==> 1
        'F600BC2D8F', # 5 > 15 ==> 0
        '9C005AC2F8F0', # 5 == 15 => 0
        '9C0141080250320F1802104A08',
        '620D49005AD2245800D0C9E72BD279CAFB0016B1FA2B1802DC00D0CC611A47FCE2A4ACE1DD144BFABBFACA002FB2C6F33DFF4A0C0119B169B013005F003720004263644384800087C3B8B51C26B449130802D1A0068A5BD7D49DE793A48B5400D8293B1F95C5A3005257B880F5802A00084C788AD0440010F8490F608CACE034401AB4D0F5802726B3392EE2199628CEA007001884005C92015CC8051800130EC0468A01042803B8300D8E200788018C027890088CE0049006028012AB00342A0060801B2EBE400424933980453EFB2ABB36032274C026E4976001237D964FF736AFB56F254CB84CDF136C1007E7EB42298FE713749F973F7283005656F902A004067CD27CC1C00D9CB5FDD4D0014348010C8331C21710021304638C513006E234308B060094BEB76CE3966AA007C6588A5670DC3754395485007A718A7F149CA2DD3B6E7B777800118E7B59C0ECF5AE5D3B6CB1496BAE53B7ADD78C013C00CD2629BF5371D1D4C537EA6E3A3E95A3E180592AC7246B34032CF92804001A1CCF9BA521782ECBD69A98648BC18025800F8C9C37C827CA7BEFB31EADF0AE801BA42B87935B8EF976194EEC426AAF640168CECAF84BC004AE7D1673A6A600B4AB65802D230D35CF81B803D3775683F3A3860087802132FB32F322C92A4C402524F2DE006E8000854378F710C0010D8F30FE224AE428C015E00D40401987F06E3600021D0CE3EC228DA000574E4C3080182931E936E953B200BF656E15400D3496E4A725B92998027C00A84EEEE6B347D30BE60094E537AA73A1D600B880371AA36C3200043235C4C866C018E4963B7E7AA2B379918C639F1550086064BB148BA499EC731004E1AC966BDBC7646600C080370822AC4C1007E38C428BE0008741689D0ECC01197CF216EA16802D3748FE91B25CAF6D5F11C463004E4FD08FAF381F6004D3232CC93E7715B463F780'
]

def decode(bits,joiner):

    global PACKETSTRING
    logging.debug(f"Decode: {bits}")
    offset=0
    while offset < len(bits):
        offset += decodeOne(bits[offset:])
        PACKETSTRING+=joiner
        remaining = len(bits)-offset
        logging.debug(f"Remaining bits {remaining}")
        if remaining > 0  and int(bits[offset:],2) == 0: # Padding...
            logging.debug(f"Skip padding {bits[offset:]}")
            break
    PACKETSTRING=PACKETSTRING[:-1]
    return offset


def decodeOne(bits):

    global VERSIONSUM
    global PACKETSTRING
    
    logging.debug(f"DecodeOne: {bits}")

    # Version/Type
    offset=0
    
    ver=int(bits[offset:offset+3],2)
    VERSIONSUM += ver
    offset+=3
    typ=int(bits[offset:offset+3],2)
    offset+=3    
    if typ == 4: # literal value packet
        logging.debug(f"v:{ver} t:{typ} - literal")
        offset += decodeLiteral(bits[offset:])
    else: # operator packet
        if typ == 0: # sum
            PACKETSTRING+="("
            j="+"
        elif typ == 1: # product 
            PACKETSTRING+="("
            j="*"
        elif typ == 2: # min
            j=","
            PACKETSTRING+="min(sys.maxsize," # See below... ;-)
        elif typ == 3: # max
            j=","
            PACKETSTRING+="max(-1," # Total hackage here because 'max(1)' isn't valid python...
        elif typ == 5: # gt
            PACKETSTRING+="("
            j=">"
        elif typ == 6: # lt
            PACKETSTRING+="("
            j="<"
        elif typ == 7: # eq
            PACKETSTRING+="("
            j="="
      
        logging.debug(f"v:{ver} t:{typ} - operator")
        lengthtypeid=int(bits[offset],2)
        offset += 1
        if lengthtypeid == 0:
            subpacketlen=int(bits[offset:offset+15],2)
            offset+=15
            logging.debug(f"subpacketlen:{subpacketlen}")
            offset += decode(bits[offset:offset+subpacketlen],j)
        else:
            subpacketcount=int(bits[offset:offset+11],2)
            offset+=11
            logging.debug(f"subpacketcount:{subpacketcount}")
            for i in range(subpacketcount):
                logging.debug(f"ss=={i}==>")
                offset += decodeOne(bits[offset:])
                PACKETSTRING+=j
                logging.debug(f"<=={i}==ss")
            PACKETSTRING=PACKETSTRING[:-1] # remove trailing + or , etc.
        PACKETSTRING+=")"
    logging.debug(f"<---{offset}---")
    
    return offset

def decodeLiteral(bits):
    global PACKETSTRING
    offset=0
    valbits=""
    more=1
    while more:
        chunk=bits[offset:offset+5]
        offset += 5
        valbits += chunk[1:] 
        more = int(chunk[0],2) # because 0 is False.
    logging.debug(f"val:{int(valbits,2)}")
    PACKETSTRING += str(int(valbits,2))
    return offset

l = logging.getLogger()
l.setLevel(logging.INFO) # or DEBUG

for input in inputs:
    b="".join([ format(int(x,16),'04b') for x in input]) # Hacky to avoid zeropad the overall bigInt...
    VERSIONSUM=0
    PACKETSTRING=""
    decodeOne(b)
    logging.info(f"VERSIONSUM:{VERSIONSUM}")
    PACKETSTRING = PACKETSTRING.replace("=","==")
    logging.info(f"PACKETSTRING:{PACKETSTRING}")
    logging.info(f"Evaluates to {int(eval(PACKETSTRING))}")
    logging.debug("-- end --")


