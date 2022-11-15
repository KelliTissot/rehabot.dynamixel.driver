from serial.tools import list_ports


def get_or_list_available_ports():
    ports = list_ports.comports()
    if len(ports) == 0:
        raise Exception("Nenhuma porta serial disponível!")
    if len(ports) == 1:
        return ports[0].device

    print("Portas encontradas:")
    for i, port in enumerate(ports):
        print(f"{i} = {port.device}")

    escolha = input("Escolha uma porta para conectar. [0]:")
    print(escolha)
    if escolha == None or escolha == "":
        return ports[0].device
    if int(escolha) >= len(ports):
        raise Exception("Escolha inválilda")
    return ports[int(escolha)].device 

if __name__ == "__main__":
    port = get_or_list_available_ports()
    print(port)
