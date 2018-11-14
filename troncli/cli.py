#!/usr/bin/env python3
#  _________  ____  _  __    _______   ____
# /_  __/ _ \/ __ \/ |/ /___/ ___/ /  /  _/
#  / / / , _/ /_/ /    /___/ /__/ /___/ /  
# /_/ /_/|_|\____/_/|_/    \___/____/___/
import os
import asyncio
import cbox

from troncli import utils, init, config, worker

ROOT_PATH = ''


@cbox.cmd
def init(version: str):
    """init dirs and fetch code.
    """
    init_handler = init.Init(ROOT_PATH)
    utils.progress_msg('Creating folders')
    init_handler.create_dirs()
    utils.progress_msg('Downloading release builds')
    asyncio.run(init_handler.fetch_jars(version))
    asyncio.run(init_handler.move_jars())


@cbox.cmd
def config(net_type: str, full_http_port: int, sol_http_port: int, full_grpc_port: int, sol_grpc_port: int):
    """customize config files.
    """
    config_handler = config.Config(ROOT_PATH)
    utils.progress_msg('Setting up config files')
    asyncio.run(config_handler.init())
    asyncio.run(config_handler.set_net_type(net_type))
    asyncio.run(config_handler.set_http_port(full_http_port, 'full'))
    asyncio.run(config_handler.set_http_port(sol_http_port, 'sol'))
    asyncio.run(config_handler.set_grpc_port(full_grpc_port, 'full'))
    asyncio.run(config_handler.set_grpc_port(sol_grpc_port, 'sol'))
    asyncio.run(config_handler.export())


@cbox.cmd
def run(node_type: str):
    """run nodes.
    """
    utils.progress_msg('Starting node(s)')
    worker = worker.Worker(ROOT_PATH)
    asyncio.run(worker.run(node_type))


@cbox.cmd
def stop(pid: str):
    """stop nodes.
    """
    worker = worker.Worker(ROOT_PATH)
    utils.progress_msg('Shutting down node(s)')
    asyncio.run(worker.stop(pid))


@cbox.cmd
def quick():
    utils.logo()
    init('lastest')
    config('private', 8500, 8600, 50051, 50001)
    run('full')
    run('sol')


def main():
    ROOT_PATH = os.getcwd()
    cbox.main([init, config, run, stop, quick])
    

if __name__ == '__main__':
    main()

