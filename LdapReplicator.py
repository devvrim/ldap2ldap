__author__ = 'haydar'
import ldap
import ldap.modlist as modlist
import ConfigParser
def main ():
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    masterport=config.get("port","master")
    masterserver=config.get("server","master")
    masterserver=masterserver+":"+masterport
    masteruser=config.get("user","master")
    masterpass=config.get("password","master")
    slaveport=config.get("port","slave")
    slaveserver=config.get("server","slave")
    slaveserver=slaveserver+":"+slaveport
    slaveuser=config.get("user","slave")
    slavepass=config.get("password","slave")
    try:
        l = ldap.initialize(masterserver)
        l.simple_bind_s(masteruser, masterpass)
        print "%s Baglantisi kuruldu" % masterserver
    except ldap.LDAPError, error_message:
        print "%s baglantisi kurulamadi" % error_message
    try:
        l2 = ldap.initialize(slaveserver)
        l2.simple_bind_s(slaveuser,slavepass)
        print "%s baglantisi kuruldu" % slaveserver
    except ldap.LDAPError, error_message:
        print "%s sebebiyle baglanti kurulamadi" % error_message
    try:
        for kk in range(1,10):
            baser = "base%s"%kk
            base = config.get("base",baser)
            base2=base+",dc=domains"
            scope= ldap.SCOPE_SUBTREE
            filter = "uid=*"
            retrieve_attributes = None
            count = 0
            result_set = []
            result_set2 = []
            dizii = []
            timeout = 0
            try:
                result_id = l.search(base, scope, filter,retrieve_attributes)
                while 1:
                    result_type, result_data = l.result(result_id, timeout)
                    if result_data == []:
                        break
                    else:
                        if result_type == ldap.RES_SEARCH_ENTRY:
                            result_set.append(result_data)
                if len(result_set) == 0:
                    return
                for i in range(len(result_set)):
                    for t in result_set[i]:
                        try:
                            uid= t [1] ['uid'] [0]
                            pas= t [1] ['userPassword'] [0]
                            cnn= t [1] ['cn'] [0]
                            snn= t [1] ['sn'] [0]
                            mail=t [1] ['mail'] [0]
                            try:
                                fitt="uid="+uid
                                dn=fitt+","+base2
                                lsonuc=l2.search(base2,scope,fitt,retrieve_attributes)
                                ldizi= []
                                ara,data=l2.result(lsonuc,0)
                                ldizi.append(data)
                                if (ldizi[0] == []):
                                    attrs = {}
                                    attrs['objectClass'] = ['inetOrgPerson']
                                    attrs['cn'] = cnn
                                    attrs['uid'] = uid
                                    attrs['sn'] = snn
                                    attrs['mail'] = mail
                                    attrs['userPassword'] = pas
                                    ldif = modlist.addModlist(attrs)
                                    l2.add_s(dn,ldif)
                                for y in ldizi[0]:
                                    uid2= y [1] ['uid'] [0]
                                    pas2= y [1] ['userPassword'] [0]
                            except:
                                pass
                            if (uid == uid2):
                                print "%s |  USER OK" %mail
                                if (pas == pas2):
                                    print "%s |  PASS OK" %mail
                                else:
                                    print "%s |  PASS NOK" %mail
                                    oldpw= {'userPassword':pas2}
                                    newpw= {'userPassword':pas}
                                    ldif = modlist.modifyModlist(oldpw,newpw)
                                    l2.modify_s(dn,ldif)
                            else:
                                print "%s |  USER NOK" %mail
                                attrs = {}
                                attrs['objectClass'] = ['inetOrgPerson']
                                attrs['cn'] = cnn
                                attrs['uid'] = uid
                                attrs['sn'] = snn
                                attrs['mail'] = mail
                                attrs['userPassword'] = pas
                                ldif = modlist.addModlist(attrs)
                                l2.add_s(dn,ldif)
                        except:
                            pass
            except ldap.LDAPError, error_message:
                print "%s sorgulamasi yapilirken -%s- hatasi alindi" %server, error_message
    except:
        pass
if __name__=='__main__':
    main()
